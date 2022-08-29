

window.addEventListener('scroll', () => {
    header.classList.toggle('shadow', window.scrollY > 0)
    headerNavbarDropdownContent.classList.toggle('shadow', window.scrollY > 0)

})