function openCreate() {
  document.getElementById("card-shadow").classList.remove("display-none");
  document.getElementById("create-post").classList.remove("display-none");
}

function closePopup() {
  document.getElementById("card-shadow").classList.add("display-none");
  document.getElementById("create-post").classList.add("display-none");
  document.getElementById("comment-post").classList.add("display-none");
}

function openComment() {
  document.getElementById("card-shadow").classList.remove("display-none");
  document.getElementById("comment-post").classList.remove("display-none");
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("#post-info").forEach((postDiv) => {
    const postId = postDiv.dataset.id;
    const likeForm = document.getElementById(`like-form-${postId}`);
    const shareForm = document.getElementById(`share-form-${postId}`);

    likeForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const url = likeForm.action;
      const csrfToken = likeForm.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const data = await response.json();
        if (data.status === "ok") {
          // Update tampilan like button (toggle warna atau isi SVG)
          likeForm.querySelector(".post-like-counter").innerText =
            data.total_likes;

          // Jika ingin toggle warna SVG manual:
          const svg = likeForm.querySelector("svg");
          if (data.liked) {
            svg.style.fill = "rgb(78, 113, 255)";
          } else {
            svg.style.fill = "rgb(166, 166, 166)";
          }
        }
      } catch (err) {
        console.error("Error saat mengirim like:", err);
      }
    });

    shareForm.addEventListener("submit", async function (e) {
      e.preventDefault();
      const url = shareForm.action;
      const csrfToken = shareForm.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const data = await response.json();

        if (data.status === "ok") {
          // Update tampilan like button (toggle warna atau isi SVG)
          shareForm.querySelector(".post-share-counter").innerText =
            data.total_shares;
        }
      } catch (err) {
        console.error("Error saat mengirim like:", err);
      }
    });
  });

  document.querySelectorAll("#comment-button").forEach((btn) => {
    btn.addEventListener("click", async function () {
      const postId = btn.dataset.postId;

      try {
        const response = await fetch(`/get_post_comment/${postId}/`, {
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        });
        const data = await response.json();
        document.querySelector("#show-date").innerText = data.post.pub_date;
        document.querySelector("#show-konten p").innerText = data.post.konten;
        document.querySelector("#show-total-like").innerText =
          data.post.total_like;
        document.querySelector("#show-total-comment").innerText =
          data.post.total_comment;
        document.querySelector("#show-total-share").innerText =
          data.post.total_share;

        const container = document.getElementById("comment-list");
        container.innerHTML = "";
        data.comments.forEach((comment) => {
          const commentCard = document.createElement("div");
          commentCard.classList.add("comment-data");
          commentCard.innerHTML = `
                  <img
                    src="/static/home/image/dummyprofile.webp"
                    class="image-icon-rounded"
                  />
                  <div class="comment-card">
                    <div class="comment-profile">
                      <h1>Davidis</h1>
                      <p>${comment.pub_date}</p>
                    </div>
                    <p>${comment.komentar}</p>
                  </div>
              `;
          container.appendChild(commentCard);
        });
      } catch (err) {
        console.error("Gagal memuat data komentar/post:", err);
      }

      const commentForm = document.getElementById("comment-form");
      commentForm.action = `/comment/${postId}/`;
      commentForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        const komentar = document.querySelector("#komentar-input").value;
        const url = commentForm.action;
        const csrfToken = commentForm.querySelector(
          "[name=csrfmiddlewaretoken]"
        ).value;

        try {
          const response = await fetch(url, {
            method: "POST",
            headers: {
              "X-CSRFToken": csrfToken,
              "X-Requested-With": "XMLHttpRequest",
            },
            body: JSON.stringify({ komentar: komentar }),
          });
          const data = await response.json();
          document.querySelector("#komentar-input").value = "";
          const container = document.getElementById("comment-list");
          container.innerHTML = "";
          data.comments.forEach((comment) => {
            const commentCard = document.createElement("div");
            commentCard.classList.add("comment-data");
            commentCard.innerHTML = `
                  <img
                    src="/static/home/image/dummyprofile.webp"
                    class="image-icon-rounded"
                  />
                  <div class="comment-card">
                    <div class="comment-profile">
                      <h1>Davidis</h1>
                      <p>${comment.pub_date}</p>
                    </div>
                    <p>${comment.komentar}</p>
                  </div>
              `;
            container.appendChild(commentCard);
          });
        } catch (err) {
          console.error("Gagal memuat data Komentar:", err);
        }
      });
    });
  });
});
