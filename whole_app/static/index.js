const body = document.body;
document.addEventListener("submit", (event) => {
  // event.preventDefault();
  let fullname = body.querySelector("#name").value;
  let number =
    body.querySelector("#country-code").value +
    body.querySelector("#phone").value;
  let gender = body.querySelector("#gender").value;
  let dob = body.querySelector("#date-of-birth").value;
  // console.log(new Date(dob));
});
