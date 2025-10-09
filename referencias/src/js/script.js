const content = document.querySelector('[wm-content]')

// carrega a página inicial
fetch('src/html/main.html')
    .then(resp => resp.text())
    .then(html => content.innerHTML = html)
    .catch(() => content.innerHTML = '<h1>Página não encontrada</h1>')

// adiciona evento nos links
document.querySelectorAll('a[wm-nav]').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault()

        const page = link.getAttribute('wm-nav')

        fetch(`src/html/${page}.html`)
            .then(resp => resp.text())
            .then(html => content.innerHTML = html)
            .catch(() => content.innerHTML = '<h1>Página não encontrada</h1>')
    })
})
