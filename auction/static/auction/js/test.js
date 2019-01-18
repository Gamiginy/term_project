/* You need to set these at last of a document. */

function offRadio() {
  var radios = document.querySelectorAll('[name="menu"]');
  for(i=0; i<radios.length; i++){
    radios[i].checked = false;
  }
}

document.getElementById('menu_btn_tgl').addEventListener('click', offRadio);