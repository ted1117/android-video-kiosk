(function () {
    const overlay = document.getElementById("player-overlay");
    const player = document.getElementById("video-player");
    const btnClose = document.getElementById("btn-close");

    function playVideo(path, name) {
        player.src = "/stream/" + path;

        overlay.style.display = "flex";
        overlay.setAttribute("aria-hidden", "false");

        player.play().catch(function () {
            // 자동재생이 막히면 컨트롤로 재생
        });

    }

    function closePlayer() {
        player.pause();
        player.removeAttribute("src");
        player.load();

        overlay.style.display = "none";
        overlay.setAttribute("aria-hidden", "true");
    }

    // 카드 클릭/키보드 접근
    document.querySelectorAll(".video-card").forEach((card) => {
        const path = card.dataset.path;
        const name = card.dataset.name;

        card.addEventListener("click", () => playVideo(path, name));
        card.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                playVideo(path, name);
            }
        });
    });

    // 닫기 버튼/확인 모달
    btnClose.addEventListener("click", closePlayer);

    // ESC로 닫기(확인창)
    window.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && overlay.style.display === "block") closePlayer();
    });
})();
