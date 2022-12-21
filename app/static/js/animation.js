var typed = new Typed('.auto-type', {
    strings: ['universe', 'world', 'continent', 'country', 'state', 'city'],
    typeSpeed: 150,
    backSpeed: 150,
    loop: true
});

var textWrapper = document.querySelector('.title-container .letters');
textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: false})
  .add({
    targets: '.title-container .letter',
    scale: [0.3,1],
    opacity: [0,1],
    translateZ: 0,
    easing: "easeOutExpo",
    duration: 600,
    delay: (el, i) => 70 * (i+1)
  }).add({
    targets: '.title-container .line',
    scaleX: [0,1],
    opacity: [0.5,1],
    easing: "easeOutExpo",
    duration: 700,
    offset: '-=875',
  });