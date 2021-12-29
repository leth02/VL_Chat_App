"use strict";
// =============== SIGN IN ===============
// TODO: Write smthg here
var signin_box = document.getElementById("signin-box");
var signin = document.getElementById("signin");
signin.onclick = function () {
  if (signin_box.style.display === "none") {
    signin_box.style.display = "block";
  }
  if (signup_box.style.display != "none") {
    signup_box.style.display = "none";
  }
};
// =============== SIGN UP ===============
// TODO: Write smthg here
var signup_box = document.getElementById("signup-box");
var signup = document.getElementById("signup");
signup.onclick = function () {
  if (signup_box.style.display === "none") {
    signup_box.style.display = "block";
  }
  if (signin_box.style.display != "none") {
    signin_box.style.display = "none";
  }
};
