var i = 0;

function typeWriter() {
    var txt = 'Theodor Hui Ren Baur';
    var speed = 25;
    if (i < txt.length) {
        document.getElementById(">name").innerHTML += txt.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
}
typeWriter();