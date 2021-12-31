'use strict';
// =============== SIGN IN ===============
// TODO: Write smthg here

// =============== SIGN UP ===============
// TODO: Write smthg here

(function () {
  console.log('Placeholder for JavaScript scripts');
  // TODO: Write smthg here

  // ** Returns eventListener 
  // @param {string} type - the type of eventListener
  // @param {string} selector - the selector of element having events
  // @param {function} callback - the callback function 

  function addGlobalEventListener(type, selector, callback) {
    document.addEventListener(type, e => {
      if (e.target.matches(selector)) callback(e)
    })
  }


  let convosItem = document.getElementsByClassName('convos-item');
  convosItem.addEventListener('click', function(e) {
    // load convos 
  })

// Right column of chat app



})();


