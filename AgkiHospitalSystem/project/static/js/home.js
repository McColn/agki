const mcColn = document.querySelector(".toggle-btn");

mcColn.addEventListener("click", function () {
    document.querySelector(".sidebar").classList.toggle("expand");
});

const items = document.querySelectorAll(".has-dropdown");

function toggle(){
    const itemToggle = this.classList.contains("active");
    for(i=0;i<items.length;i++){
        items[i].classList.remove("active");
    }
    if (!itemToggle){
        this.classList.add("active");
    }
}
items.forEach((item)=> item.addEventListener("click", toggle));



