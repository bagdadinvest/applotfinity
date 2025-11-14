document.addEventListener("DOMContentLoaded", function() {
    const globeContainer = document.getElementById("globe-container");
    const globeTrigger = document.getElementById("globeTrigger");
    const languageSwitcherContainer = document.getElementById("language-switcher-container");
    const closeGlobe = document.getElementById("closeGlobe");
    const backgroundOverlay = document.getElementById("background-overlay");

    // Initialize the Globe
    const world = Globe()(globeContainer)
        .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
        .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png');

    // Button click event to show the Globe
    globeTrigger.addEventListener("click", () => {
        languageSwitcherContainer.classList.remove("hidden");
        backgroundOverlay.classList.remove("hidden");
        setTimeout(() => {
            languageSwitcherContainer.style.opacity = "1";
            backgroundOverlay.style.opacity = "0.5";
        }, 100);
    });

    // Button click event to hide the Globe
    closeGlobe.addEventListener("click", () => {
        languageSwitcherContainer.style.opacity = "0";
        backgroundOverlay.style.opacity = "0";
        setTimeout(() => {
            languageSwitcherContainer.classList.add("hidden");
            backgroundOverlay.classList.add("hidden");
        }, 500);
    });

    // Click event on background overlay to hide the Globe
    backgroundOverlay.addEventListener("click", () => {
        closeGlobe.click();
    });

    // Auto-Rotation & Hover Effects
    let autoRotate = true;
    function rotateGlobe() {
        if (autoRotate) {
            const currView = world.pointOfView();
            world.pointOfView(
                { lat: currView.lat, lng: currView.lng + 0.5, altitude: currView.altitude },
                100
            );
            setTimeout(rotateGlobe, 100);
        }
    }

    rotateGlobe();
    globeContainer.addEventListener("mouseover", () => { autoRotate = false; });
    globeContainer.addEventListener("mouseout", () => {
        autoRotate = true;
        rotateGlobe();
    });
});
