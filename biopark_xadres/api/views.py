# views.py - Versão com melhor debug e tratamento

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
import uuid
import chess
import chess.engine
from datetime import datetime

# Dicionário para armazenar jogos em memória (em produção, use Redis ou DB)
GAMES_STORAGE = {}

def index(request):
    return render(request, 'api/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def start_game(request):
    try:
        data = json.loads(request.body)
        player_color = data.get('player_color')
        print(f"[DEBUG] Starting game with player color: {player_color}")
        
        if player_color not in ['white', 'black']:
            return JsonResponse({'error': 'Cor inválida. Use "white" ou "black"'}, status=400)
        
        # Cria novo jogo
        game_id = str(uuid.uuid4())
        board = chess.Board()  # Posição inicial
        
        # Armazena o jogo
        GAMES_STORAGE[game_id] = {
            'board': board,
            'player_color': player_color,
            'status': 'playing',
            'pgn': '',
            'move_count': 0,
            'created_at': datetime.now()
        }
        
        print(f"[DEBUG] Initial board FEN: {board.fen()}")
        
        # Se jogador escolheu pretas, IA joga primeiro
        if player_color == 'black':
            ai_move = get_ai_move(board)
            if ai_move:
                print(f"[DEBUG] AI first move: {ai_move}")
                board.push(ai_move)
                GAMES_STORAGE[game_id]['board'] = board
                GAMES_STORAGE[game_id]['move_count'] = 1
        
        current_turn = 'white' if board.turn else 'black'
        response_data = {
            'game_id': game_id,
            'board': board.fen(),
            'turn': current_turn,
            'status': get_game_status(board),
            'pgn': board_to_pgn(board)
        }
        
        print(f"[DEBUG] Game started successfully: {response_data}")
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        print(f"[ERROR] Start game error: {str(e)}")
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)

@csrf_exempt 
@require_http_methods(["POST"])
def make_move(request, game_id):
    try:
        if game_id not in GAMES_STORAGE:
            return JsonResponse({'error': 'Jogo não encontrado'}, status=404)
        
        data = json.loads(request.body)
        move_str = data.get('move')
        print(f"[DEBUG] Player move attempt: {move_str}")
        
        if not move_str:
            return JsonResponse({'error': 'Movimento não fornecido'}, status=400)
        
        game = GAMES_STORAGE[game_id]
        board = game['board']
        player_color = game['player_color']
        
        # Verifica se é a vez do jogador
        current_turn = 'white' if board.turn else 'black'
        if current_turn != player_color:
            return JsonResponse({'error': 'Não é sua vez'}, status=400)
        
        # Tenta fazer o movimento do jogador
        try:
            move = parse_move(board, move_str)
            if move not in board.legal_moves:
                return JsonResponse({'error': 'Movimento ilegal'}, status=400)
                
            board.push(move)
            game['move_count'] += 1
            print(f"[DEBUG] Player move made: {move}, new FEN: {board.fen()}")
            
        except ValueError as e:
            return JsonResponse({'error': f'Movimento inválido: {str(e)}'}, status=400)
        
        # Verifica status após movimento do jogador
        game_status = get_game_status(board)
        if game_status in ['checkmate', 'stalemate', 'draw']:
            game['status'] = game_status
            response_data = {
                'success': True,
                'board': board.fen(),
                'turn': 'white' if board.turn else 'black',
                'status': game_status,
                'pgn': board_to_pgn(board),
                'ai_move': None
            }
            print(f"[DEBUG] Game ended: {response_data}")
            return JsonResponse(response_data)
        
        # IA faz sua jogada
        ai_move = get_ai_move(board)
        ai_move_str = None
        
        if ai_move:
            ai_move_str = str(ai_move)
            board.push(ai_move)
            game['move_count'] += 1
            print(f"[DEBUG] AI move made: {ai_move}, new FEN: {board.fen()}")
        
        # Atualiza status final
        game_status = get_game_status(board)
        game['status'] = game_status
        
        response_data = {
            'success': True,
            'board': board.fen(),
            'turn': 'white' if board.turn else 'black',
            'status': game_status,
            'pgn': board_to_pgn(board),
            'ai_move': ai_move_str
        }
        
        print(f"[DEBUG] Move completed: {response_data}")
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        print(f"[ERROR] Make move error: {str(e)}")
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)

@require_http_methods(["GET"])
def game_status(request, game_id):
    try:
        if game_id not in GAMES_STORAGE:
            return JsonResponse({'error': 'Jogo não encontrado'}, status=404)
        
        game = GAMES_STORAGE[game_id]
        board = game['board']
        
        response_data = {
            'board': board.fen(),
            'turn': 'white' if board.turn else 'black',
            'status': get_game_status(board),
            'pgn': board_to_pgn(board),
            'move_count': game['move_count']
        }
        
        print(f"[DEBUG] Status request for {game_id}: {response_data}")
        return JsonResponse(response_data)
        
    except Exception as e:
        print(f"[ERROR] Game status error: {str(e)}")
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)

# === FUNÇÕES AUXILIARES ===

def parse_move(board, move_str):
    """
    Converte string de movimento para objeto Move
    Aceita formatos: UCI (e2e4), SAN (Nf3), coordenadas (e2-e4)
    """
    move_str = move_str.strip().replace('-', '').replace('x', '').replace('+', '').replace('#', '')
    
    try:
        # Tenta UCI primeiro (e2e4, e7e8q)
        move = chess.Move.from_uci(move_str)
        print(f"[DEBUG] Parsed as UCI: {move_str} -> {move}")
        return move
    except ValueError:
        pass
    
    try:
        # Tenta SAN (Nf3, O-O, e4)
        move = board.parse_san(move_str)
        print(f"[DEBUG] Parsed as SAN: {move_str} -> {move}")
        return move
    except ValueError:
        pass
    
    raise ValueError(f"Formato de movimento não reconhecido: {move_str}")

def get_ai_move(board):
    """
    Retorna movimento da IA usando algoritmo simples
    Em produção, use Stockfish ou outra engine
    """
    if board.is_game_over():
        return None
    
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
    
    print(f"[DEBUG] AI evaluating {len(legal_moves)} legal moves")
    
    # IA simples: prioriza capturas, depois movimentos centrais
    scored_moves = []
    
    for move in legal_moves:
        score = 0
        
        # Bonifica capturas
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                piece_values = {
                    chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
                    chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
                }
                capture_value = piece_values.get(captured_piece.piece_type, 0)
                score += capture_value * 10
                print(f"[DEBUG] Capture bonus for {move}: +{capture_value * 10}")
        
        # Bonifica movimentos para o centro
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        if move.to_square in center_squares:
            score += 2
            print(f"[DEBUG] Center bonus for {move}: +2")
        
        # Bonifica xeques
        board.push(move)
        if board.is_check():
            score += 5
            print(f"[DEBUG] Check bonus for {move}: +5")
        board.pop()
        
        scored_moves.append((move, score))
    
    # Ordena por score e pega o melhor
    scored_moves.sort(key=lambda x: x[1], reverse=True)
    
    # Log dos melhores movimentos
    print(f"[DEBUG] Top 3 AI moves: {[(str(m), s) for m, s in scored_moves[:3]]}")
    
    # Adiciona um pouco de randomização nos melhores movimentos
    import random
    best_score = scored_moves[0][1]
    best_moves = [move for move, score in scored_moves if score >= best_score - 1]
    
    selected_move = random.choice(best_moves)
    print(f"[DEBUG] AI selected move: {selected_move}")
    return selected_move

def get_game_status(board):
    """Retorna status atual do jogo"""
    if board.is_checkmate():
        return 'checkmate'
    elif board.is_stalemate():
        return 'stalemate' 
    elif board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 'draw'
    elif board.is_check():
        return 'check'
    else:
        return 'playing'

def board_to_pgn(board):
    """Converte board para notação PGN"""
    if not board.move_stack:
        return "Nenhuma jogada ainda"
    
    pgn_moves = []
    temp_board = chess.Board()
    
    for i, move in enumerate(board.move_stack):
        if i % 2 == 0:  # Movimento das brancas
            move_number = (i // 2) + 1
            pgn_moves.append(f"{move_number}. {temp_board.san(move)}")
        else:  # Movimento das pretas
            pgn_moves.append(temp_board.san(move))
        
        temp_board.push(move)
    
    return ' '.join(pgn_moves)

# Função para limpar jogos antigos (rode em uma task periódica)
def cleanup_old_games():
    """Remove jogos mais antigos que 1 hora"""
    from datetime import timedelta
    cutoff_time = datetime.now() - timedelta(hours=1)
    
    games_to_remove = [
        game_id for game_id, game in GAMES_STORAGE.items()
        if game['created_at'] < cutoff_time
    ]
    
    for game_id in games_to_remove:
        del GAMES_STORAGE[game_id]
    
    print(f"[DEBUG] Removidos {len(games_to_remove)} jogos antigos")