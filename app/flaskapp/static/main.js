const alertEl = document.querySelector('.alert');
console.log(alertEl)
if (alertEl) {
    setTimeout(function(){
        alertEl.setAttribute("style","display:none;");;
    },3000)
}
console.log('Done')