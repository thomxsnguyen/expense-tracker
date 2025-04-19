document.addEventListener("DOMContentLoaded", function () {
  const registerBtn = document.getElementById("register");
  const loginBtn = document.getElementById("login");

  const createAcc = document.getElementById("create_account");
  const loginAcc = document.getElementById("login_account");

  registerBtn.addEventListener("click", function () {
    const register_view = document.getElementById("register-view");
    document.getElementById("login-view").style.display = "none";

    createAcc.style.display = "flex";
    loginAcc.style.display = "none";

    register_view.style.display = "block";
    register_view.classList.add("vertical-flex");
  });

  loginBtn.addEventListener("click", function () {
    const login_view = document.getElementById("login-view");
    document.getElementById("register-view").style.display = "none";

    createAcc.style.display = "none";
    loginAcc.style.display = "flex";

    login_view.style.display = "block";
    login_view.classList.add("vertical-flex");
  });

  createAcc.addEventListener("click", function (event) {
    event.preventDefault();

    const new_username = document.getElementById("new_username").value;
    const new_password = document.getElementById("new_password").value;
    const profile = { user: new_username, password: new_password };
    fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify(profile),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      })
      .catch((err) => {
        console.error("ERROR:", err);
      });
  });

  loginAcc.addEventListener("click", function (event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const profile = { user: username, password: password };
    fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-type": "application/json" },
      body: JSON.stringify(profile),
    })
      .then((response) => response.json())
      .then((data) => {
        const token = data.token;
        localStorage.setItem("token", token);
        document.getElementById("login-view").style.display = "none";
        document.querySelectorAll(".button-group").forEach((el) => {
          el.classList.toggle("hidden");
        });
        document.querySelectorAll(".acc-button").forEach((el) => {
          el.classList.toggle("hidden");
        });
        document.querySelectorAll(".button-expenses").forEach((el) => {
          el.classList.toggle("hidden");
        });
      })
      .catch((err) => {
        console.error("ERROR:", err);
      });
  });

  const addExp = document.getElementById("create-expense");
  addExp.addEventListener("click", function (event) {
    event.preventDefault();
    document.querySelectorAll(".button-expenses").forEach((el) => {
      el.classList.toggle("hidden");
    });
    document.querySelectorAll(".create-expense").forEach((el) => {
      el.classList.toggle("hidden");
    });

    // const description = document.getElementById("description").value;
    // const category = document.getElementById("category").value;
    // const price = document.getElementById("price").value;

    // const body = { description: description, category: category, price: price };

    // const token = localStorage.getItem("token");
    // fetch("http://127.0.0.1:5000/expense", {
    //   method: "GET",
    //   headers: {
    //     Authorization: `Bearer ${token}`,
    //     "Content-Type": "application/json",
    //     body: JSON.stringify(body),
    //   },
    // }).then(((response) => response.json()).then((data) => console.log(data)));
  });
});
