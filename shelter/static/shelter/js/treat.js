let treatBtn = document.getElementById("treat")
let eatText = document.getElementById("eat")
// simple JS to use a button to give an animal a treat. when you click the button test appears that say it way yummy
treatBtn.addEventListener("click", ()=> {
    eatText.innerText = "That was yummy!"
    console.log("Hello")
})