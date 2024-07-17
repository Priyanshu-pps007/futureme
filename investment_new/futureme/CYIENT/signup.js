document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("authForm");
    const passwordInput = document.querySelector(
      'input[placeholder="Login password"]'
    );
    const verifyPasswordInput = document.querySelector(
      'input[placeholder="re-enter the same password"]'
    );
    const transactionPasswordInput = document.querySelector(
      'input[placeholder="Transaction Password"]'
    );
    const verifyTransactionPasswordInput = document.querySelector(
      'input[placeholder="Re-enter Transaction Password"]'
    );
    const mobileInput = document.querySelector(
      'input[placeholder="Mobile number"]'
    );
    const otpInput = document.querySelector('input[placeholder="OTP"]');
    const invitationalCodeInput = document.querySelector(
      'input[placeholder="Invitational code"]'
    );
    const alertMessage = document.getElementById("alertMessage");
    const messageContent = alertMessage.querySelector(".message-content");
    const closeButton = document.querySelector(
      ".close-button[data-close='true']"
    );
    const verifyBtn = document.getElementById("verifyBtn");
    const togglePassword1 = document.getElementById("togglePassword1");
    const togglePassword2 = document.getElementById("togglePassword2");
  
    function validatePassword(input1, input2) {
      if (input1.value !== input2.value) {
        showAlert(
          "The Login Password and its confirmation do not match. Please try again."
        );
        return false;
      }
      return true;
    }
    function validatePassword2(input1, input2) {
      if (input1.value !== input2.value) {
        showAlert(
          "The Transaction Password and its confirmation do not match. Please try again."
        );
        return false;
      }
      return true;
    }
  
    function validateMobileNumber(input) {
      const mobileRegex = /^[0-9]{10}$/;
      if (!mobileRegex.test(input.value)) {
        showAlert("Invalid mobile number");
        return false;
      }
      return true;
    }
  
    function validateOTP(input) {
      const otpRegex = /^[0-9]{6}$/;
      if (!otpRegex.test(input.value)) {
        showAlert("Invalid OTP");
        return false;
      }
      return true;
    }
  
    // Simplified password validation for 8 characters only
    function validatePasswordStrength(input) {
      if (input.value.length < 8) {
        showAlert(
          "Password must be at least 8 characters long."
        );
        return false;
      }
      return true;
    }
  
    function validatePasswordsNotSame(passwordInput, transactionPasswordInput) {
      if (passwordInput.value === transactionPasswordInput.value) {
        showAlert(
          "Login password and Transaction password cannot be the same. Please choose different passwords."
        );
        return false;
      }
      return true;
    }
  
    function validateForm() {
      return (
        validatePassword(passwordInput, verifyPasswordInput) && // Validates login password
        validatePassword2(
          transactionPasswordInput,
          verifyTransactionPasswordInput
        ) && // Validates transaction password
        validateMobileNumber(mobileInput) &&
        validateOTP(otpInput) &&
        validatePasswordStrength(passwordInput) &&
        validatePasswordsNotSame(passwordInput, transactionPasswordInput)
      );
    }
  
    function showAlert(message) {
      messageContent.textContent = message;
      alertMessage.classList.add("show");
    }
  
    function closeAlert() {
      alertMessage.classList.remove("show");
    }
  
    form.addEventListener("submit", function (event) {
      if (!validateForm()) {
        event.preventDefault(); // Prevent form submission if invalid
      } else {
        // Redirect to login page AFTER successful form submission
        alert("SIGNUP SUCESSFULL! You can now proceed to Login Page");
      }
    });
    closeButton.addEventListener("click", closeAlert);
  
    function generateOTP() {
      let otp = "";
      for (let i = 0; i < 6; i++) {
        otp += Math.floor(Math.random() * 10); // Generate a random digit (0-9)
      }
      return otp;
    }
  
    verifyBtn.addEventListener("click", function () {
      if (validateMobileNumber(mobileInput)) {
        const generatedOTP = generateOTP();
        otpInput.value = generatedOTP;
      } else {
        showAlert("Please enter a valid mobile number first.");
      }
    });
  
    function togglePassword(inputField, toggleButton) {
      if (inputField.type === "password") {
        inputField.type = "text";
        toggleButton.innerHTML = `<img aria-hidden="true" alt="eye" src="https://img.icons8.com/?size=16&id=121557&format=png&color=ffffff" />`; // Closed eye icon
      } else {
        inputField.type = "password";
        toggleButton.innerHTML = `<img aria-hidden="true" alt="eye" src="https://img.icons8.com/?size=16&id=60022&format=png&color=ffffff" />`; // Open eye icon
      }
    }
  
    // Add event listeners to the toggle buttons
    togglePassword1.addEventListener("click", function () {
      togglePassword(passwordInput, togglePassword1);
    });
    togglePassword2.addEventListener("click", function () {
      togglePassword(verifyPasswordInput, togglePassword2);
    });
  });