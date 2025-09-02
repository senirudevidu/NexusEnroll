// Fix for faculty dashboard course display

// Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Set a timeout to ensure everything is loaded
  setTimeout(function () {
    // Make sure the "my-courses" tab is properly initialized even if not active
    const myCoursesTab = document.getElementById("my-courses");
    if (myCoursesTab) {
      console.log("Initializing my-courses tab");

      // Force the container to be visible briefly to ensure cards are rendered
      const originalDisplay = myCoursesTab.style.display;
      const originalVisibility = myCoursesTab.style.visibility;

      // Make it visible but hidden to trigger card rendering
      myCoursesTab.style.display = "block";
      myCoursesTab.style.visibility = "hidden";

      // Force layout recalculation
      setTimeout(function () {
        // Reset to original state
        myCoursesTab.style.display = originalDisplay;
        myCoursesTab.style.visibility = originalVisibility;

        console.log("My courses tab has been initialized");
      }, 100);
    }

    // Fix tab switching by adding direct event listeners
    document.querySelectorAll(".tab-button").forEach(function (button) {
      button.addEventListener("click", function () {
        const tabId = this.getAttribute("onclick")
          .toString()
          .match(/openTab\(['"]([^'"]+)['"]/)[1];
        if (tabId) {
          console.log("Tab clicked:", tabId);

          // Hide all tab panes
          document.querySelectorAll(".tab-pane").forEach(function (pane) {
            pane.style.display = "none";
            pane.classList.remove("active");
          });

          // Show clicked tab
          const targetPane = document.getElementById(tabId);
          if (targetPane) {
            targetPane.style.display = "block";
            targetPane.classList.add("active");

            // Special handling for my-courses tab
            if (tabId === "my-courses") {
              console.log("Refreshing course cards");
              if (typeof populateCourseCards === "function") {
                populateCourseCards();
              }
            }
          }

          // Update active button
          document.querySelectorAll(".tab-button").forEach(function (btn) {
            btn.classList.remove("active");
          });
          this.classList.add("active");
        }
      });
    });
  }, 500);
});

// Add a global function to force reload course cards
window.refreshCourseCards = function () {
  console.log("Manual refresh of course cards triggered");
  if (typeof populateCourseCards === "function") {
    populateCourseCards();
  }
};
