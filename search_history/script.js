const buttons = document.querySelectorAll(".modalBtn");

buttons.forEach((button) => {
  button.onclick = function () {
    const index = button.id.slice(3);
    const windowID = "modal" + index;
    const openedWindow = document.getElementById(windowID);
    const closeBtn = openedWindow.querySelector(".close");

    openedWindow.style.display = "flex";

    closeBtn.onclick = function () {
      openedWindow.style.display = "none";
    };

    window.onclick = function (event) {
      if (event.target === openedWindow) {
      openedWindow.style.display = "none";
      }
    };

    window.addEventListener("keydown", function (event) {
      if (event.key === "Escape" || event.code === "Escape") {
        openedWindow.style.display = "none";
      }
    });
  };
});
