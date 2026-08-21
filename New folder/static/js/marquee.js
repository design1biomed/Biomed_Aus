const track = document.querySelector(".marquee-track");

let pressed = false;
let startX = 0;
let currentTranslate = 0;

track.addEventListener("mousedown", e => {
    pressed = true;
    track.style.animationPlayState = "paused";

    startX = e.clientX;
});

window.addEventListener("mouseup", () => {
    pressed = false;
    track.style.animationPlayState = "running";
});

window.addEventListener("mousemove", e => {

    if(!pressed) return;

    const walk = e.clientX - startX;

    track.style.transform =
        `translateX(${currentTranslate + walk}px)`;
});