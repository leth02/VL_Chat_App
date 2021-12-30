"use strict";
// =============== SIGN IN ===============
// TODO: Write smthg here
var signin_box = document.getElementsByClassName("signin-box");
var in_to_up = document.getElementById("switch-in-to-up");
in_to_up.onclick = function () {
  signin_box[0].classList.toggle("show");
  signup_box[0].classList.toggle("hide");

  signin_box[0].classList.toggle("hide");
  signup_box[0].classList.toggle("show");
};

// =============== SIGN UP ===============
// TODO: Write smthg here
var signup_box = document.getElementsByClassName("signup-box");
var up_to_in = document.getElementById("switch-up-to-in");
up_to_in.onclick = function () {
  signin_box[0].classList.toggle("show");
  signup_box[0].classList.toggle("hide");

  signup_box[0].classList.toggle("show");
  signin_box[0].classList.toggle("hide");
};
