const spinner = document.querySelector('.spinner');
const mainContent = document.getElementById('main-content');

window.addEventListener('load', () => {
    spinner.style.display = 'none';
    mainContent.style.display = 'block';
});

window.addEventListener('submit', () => {
    spinner.style.display = 'block';
    mainContent.style.display = 'none';
});

document.querySelectorAll('a').forEach(link => {
link.addEventListener('click', () => {
    spinner.style.display = 'block';
    mainContent.style.display = 'none';
})
});


