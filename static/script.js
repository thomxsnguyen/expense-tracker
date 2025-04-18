document.addEventListener("DOMContentLoaded", function () {
  const registerBtn = document.getElementById("register");
  const loginBtn = document.getElementById("login");

  registerBtn.addEventListener("click", function () {
    document.getElementById("login-view").style.display = "none";
    const register_view = document.getElementById("register-view");
    register_view.style.display = "block";
    register_view.classList.add("vertical-flex");
  });

  loginBtn.addEventListener("click", function () {
    document.getElementById("register-view").style.display = "none";
    const login_view = document.getElementById("login-view");
    login_view.style.display = "block";
    login_view.classList.add("vertical-flex");

    const 
  });
});
