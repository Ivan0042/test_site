let audio = new Audio();
let typeVolume = '<span class="material-icons">volume_up</span>'
let seekto
const playBtn = document.querySelector("#now_sound")
const nextBtn = document.querySelector("#next_sound")
const pregBtn = document.querySelector("#preg_sound")
const muteBtn = document.querySelector("#mute_sound")
const seekSlider = document.querySelector("#slider")
const volumeSlider = document.querySelector("#volume_slider")
let seeking = false
const curTimeText = document.querySelector("#current_time")
const durTimeText = document.querySelector("#time_sound")
const volumeText = document.querySelector("#volume_text")

playList = ["lol", "pop", "info"]

audio.src = "/static/sound/2f2747bab958b9700b61200399c331.mp3"
audio.loop = false

playBtn.addEventListener("click", playPause);
nextBtn.addEventListener("click", nextSound);
pregBtn.addEventListener("click", pregSound);
muteBtn.addEventListener("click", muteSound);
seekSlider.addEventListener("mousedown", (e)=>{
    seeking = true;
    audio.muted = true
    seek(e);
});
seekSlider.addEventListener("mousemove", (e)=>{seek(e)});
seekSlider.addEventListener("mouseup", ()=>{
    seeking = false
    audio.muted = false});
volumeSlider.addEventListener("mousemove", setVolume)
audio.addEventListener("timeupdate", ()=>{seekTimeUpdate()});
audio.addEventListener("ended", ()=>{switchSound()});

function timeSoundView(time){
    const min = Math.floor(time / 60)
    let second = Math.floor(time - min * 60)
    if(second < 10)
        second = `0${second}`
    
    return `${min}:${second}`
}

function updateIconVolume(type){
    muteBtn.childNodes[1].innerHTML = type
    menuVolume.childNodes[5].innerHTML = type
}

function playPause(){
    if(audio.paused){
        audio.play();
        playBtn.innerHTML = '<span class="material-icons">pause</span>'
    }else{
        audio.pause();
        playBtn.innerHTML = '<span class="material-icons">play_arrow</span>'
    }
    durTimeText.innerHTML = timeSoundView(audio.duration)
}

function nextSound(){

}

function pregSound(){

}

function setVolume(){
    audio.volume = volumeSlider.value / 100
    volumeText.innerHTML = volumeSlider.value
    if(50 <= volumeSlider.value <= 100){
        typeVolume = "volume_up"
    }else if(0 < volumeSlider.value < 50){
        typeVolume = "volume_down"
    }else{
        typeVolume = "volume_mute"
    }
    updateIconVolume(typeVolume)
}

function muteSound(){
    if(audio.muted){
        audio.muted = false
        typeVolume = 'volume_up'
    }else{
        audio.muted = true
        typeVolume = 'volume_off'
    }
    updateIconVolume(typeVolume)
}

function seekTimeUpdate(){

}

function switchSound(){

}

function seek(e){
    if(audio.duration == 0){
        null
    }else{
        if(seeking){
            seekSlider.value = (e.clientX - seekSlider.offsetLeft) / (seekSlider.offsetWidth - 0)
            seekto = seekSlider.value * audio.duration
            audio.currentTime = seekto
            curTimeText.innerHTML = timeSoundView(audio.currentTime)
        }
    }
}

function seekTimeUpdate(){
    if(audio.duration){
        if(seeking == false){
            seekSlider.value = audio.currentTime * (100 / audio.duration);
            curTimeText.innerHTML = timeSoundView(audio.currentTime)
        }
    }
}

//*************************************************************/
const menuVolume = document.querySelector(".menu_right_volume")

muteBtn.addEventListener("contextmenu", (e)=>{
    e.preventDefault();
    menuVolume.style.display = "flex"
    let mod = (menuVolume.offsetWidth - muteBtn.offsetWidth) / 2
    menuVolume.style.left = `${muteBtn.offsetLeft - mod}px`
    console.log(muteBtn.getBoundingClientRect().y, menuVolume.offsetHeight)
    menuVolume.style.top = `${muteBtn.getBoundingClientRect().y - menuVolume.offsetHeight}px`
    updateIconVolume(typeVolume)
})

document.addEventListener("click", (e)=>{
    if (e.button !== 2){
        menuVolume.style.display = "none"
    }
}, false)

menuVolume.addEventListener("click", (e)=>{
    e.stopPropagation();
})

