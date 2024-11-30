document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.skills');
    const btnScrollLeft = document.getElementById('btn-scroll-left');
    const btnScrollRight = document.getElementById('btn-scroll-right');

    btnScrollLeft.addEventListener('click', () => {
        container.scrollBy({ left: -100, behavior: 'smooth' });
    });

    btnScrollRight.addEventListener('click', () => {
        container.scrollBy({ left: 100, behavior: 'smooth' });
    });
});