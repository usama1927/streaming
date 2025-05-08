$(document).ready(() => {
  const token = localStorage.getItem("token");
  const user = parseJwt(token);
  if (!user || user.role !== "consumer") {
    alert("Login as a consumer to view the feed");
    window.location.href = "/login";
  }

  let currentIndex = 0;
  let videos = [];

  function loadNextVideo() {
    if (currentIndex >= videos.length) return;

    const item = videos[currentIndex];
    currentIndex++;

    const avg = item.ratings.length
      ? (item.ratings.reduce((a, b) => a + b, 0) / item.ratings.length).toFixed(1)
      : "N/A";

    const commentSection = item.comments.map(c => `<div class="mb-1">💬 ${c}</div>`).join("");

    $('#gallery').append(`
      <div class="card mb-4 shadow-sm video-card">
        <div class="card-body">
          <video controls autoplay muted class="w-100 mb-3" src="${item.url}" preload="metadata"></video>
          <h5>${item.title}</h5>
          <p class="text-muted">${item.caption || ""}</p>
          <p><strong>Location:</strong> ${item.location || "N/A"}</p>
          <p><strong>People:</strong> ${item.people || "N/A"}</p>
          <p><strong>Average Rating:</strong> ${avg}</p>

          <div class="mb-3">
            <select id="rate-${item.id}" class="form-select form-select-sm w-auto d-inline">
              <option value="1">1 ⭐</option>
              <option value="2">2 ⭐</option>
              <option value="3">3 ⭐</option>
              <option value="4">4 ⭐</option>
              <option value="5">5 ⭐</option>
            </select>
            <button class="btn btn-sm btn-outline-success" onclick="submitRating(${item.id})">Rate</button>
          </div>

          <div>
            <strong>Comments:</strong>
            <div class="mb-2 small">${commentSection || "<i class='text-muted'>No comments yet</i>"}</div>
            <input class="form-control form-control-sm mt-1" placeholder="Write a comment..." data-id="${item.id}" />
            <button class="btn btn-sm btn-outline-primary mt-1" onclick="submitComment(${item.id}, this)">Comment</button>
          </div>
        </div>
      </div>
    `);
  }

  $.get("/consumer/videos", function (data) {
    videos = data;
    if (videos.length) loadNextVideo();
  });

  // Lazy scroll loader
  $(window).scroll(() => {
    if ($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
      loadNextVideo();
    }
  });
});

function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
}

function submitComment(videoId, btn) {
  const input = $(btn).siblings("input");
  const comment = input.val();
  const token = localStorage.getItem("token");

  if (!comment.trim()) return alert("Please write a comment.");
  $.ajax({
    url: "/consumer/comment",
    method: "POST",
    headers: { Authorization: "Bearer " + token },
    data: { video_id: videoId, text: comment },
    success: () => {
      alert("Comment added");
      input.val("");
    },
    error: () => alert("Failed. Login as a consumer.")
  });
}

function submitRating(videoId) {
  const rating = $(`#rate-${videoId}`).val();
  const token = localStorage.getItem("token");

  $.ajax({
    url: "/consumer/rate",
    method: "POST",
    headers: { Authorization: "Bearer " + token },
    data: { video_id: videoId, rating_value: rating },
    success: () => alert("Rating submitted."),
    error: () => alert("Failed. Login as a consumer.")
  });
}
