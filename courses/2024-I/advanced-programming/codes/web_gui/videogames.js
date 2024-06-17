function login(){
    let username_ = document.getElementById("txtName").value
    let password_ = document.getElementById("txtPassword").value

    // JavaScrip Object
    let loginData = {
        username: username_,
        password: password_
    }

    console.log(loginData)
}