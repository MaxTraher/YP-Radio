import webview

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YP-Radio</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: url('https://d2soft.neocities.org/background.jpg') no-repeat center center fixed;
            background-size: cover;
            color: #fff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        #container {
            width: 564px;
            height: 236px;
            background: rgba(0, 0, 0, 0.7);
            padding: 5px;
            box-sizing: border-box;
            border-radius: 5px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            position: relative;
        }
        #videoSelectButton {
            position: absolute;
            top: 5px;
            right: 8px;
            background: #800000;
            border: none;
            color: #FFF;
            padding: 5px 10px;
            cursor: pointer;
            border-radius: 3px;
        }
        #videoSelectDropdown {
            position: absolute;
            top: 35px;
            right: 8px;
            background: #FFF;
            color: #000;
            padding: 5px;
            border-radius: 3px;
            display: none;
            z-index: 1000;
        }
        #videoSelectDropdown div {
            padding: 5px;
            cursor: pointer;
        }
        #videoSelectDropdown div:hover {
            background: #ccc;
        }
        #player {
            width: 100%;
            height: 0;
            margin: 0;
            padding: 0;
            background: transparent;
            border: none;
        }
        #visualizer {
            width: 100%;
            height: 60px;
            background: transparent;
            visibility: hidden;
            display: flex;
            justify-content: center;
            align-items: flex-end;
            padding-bottom: 5px;
        }
        .bar {
            width: 6px;
            height: 0;
            background: #800000;
            margin: 0 1px;
            animation: bounce 1s infinite ease-in-out;
        }
        @keyframes bounce {
            0% {
                transform: scaleY(0.5);
            }
            50% {
                transform: scaleY(1);
            }
            100% {
                transform: scaleY(0.5);
            }
        }
        #controls {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .button {
            background: #800000;
            border: none;
            color: #FFF;
            padding: 10px;
            margin: 5px;
            cursor: pointer;
            flex: 1;
            border-radius: 3px;
        }
        .button.active {
            background: #ee3a1f;
        }
        .button.muted {
            background: #ee3a1f;
        }
        .button.stop-active {
            background: #ee3a1f;
        }
        .volume-control {
            margin-left: 20px;
            display: flex;
            align-items: center;
        }
        .volume-control input {
            width: 100px;
        }
        #categoryLabel {
            margin-top: 5px;
            color: #fff;
        }
    </style>
</head>
<body>
    <div id="container">
        <button id="videoSelectButton" onclick="toggleDropdown()">Select radio</button>
        <div id="videoSelectDropdown">
            <div onclick="changeVideo('8v_kKMaq5po', 'Phonk')">Phonk</div>
            <div onclick="changeVideo('sR-sbG98ldM', 'DnB / Electro')">DnB / Electro</div>
            <div onclick="changeVideo('0veWDx5beDs', 'Dark Techno')">Dark Techno</div>
            <div onclick="changeVideo('jfKfPfyJRdk', 'Lofi hip-hop')">Lofi hip-hop</div>
            <div onclick="changeVideo('3kgNy-kvFak', 'Retro 80s 90s')">Retro 80s 90s</div>
            <div onclick="changeVideo('akHAQD3o1NA', 'GachiBass')">GachiBass</div>
        </div>
        <div id="player"></div>
        <div id="visualizer">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        <div id="categoryLabel">Current radio: Phonk</div>
        <div id="controls">
            <button class="button" id="playButton" onclick="playStream()">Play</button>
            <button class="button" id="stopButton" onclick="stopStream()">Stop</button>
            <button class="button" id="muteButton" onclick="muteUnmute()">Mute/Unmute</button>
            <div class="volume-control">
                <label for="volume">Volume:</label>
                <input type="range" id="volume" min="0" max="100" value="40" onchange="setVolume(this.value)">
            </div>
        </div>
    </div>
    <script>
        var player;
        var isMuted = false;
        var currentVideoId = '8v_kKMaq5po';
        var currentCategory = 'Phonk';

        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        function createPlayer() {
            if (player) {
                player.destroy();
            }

            player = new YT.Player('player', {
                height: '0',
                width: '0',
                videoId: currentVideoId,
                playerVars: {
                    'autoplay': 1,
                    'controls': 0,
                    'mute': isMuted ? 1 : 0,
                    'loop': 1,
                    'playlist': currentVideoId,
                    'vq': 'small'
                },
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });
        }

        function onYouTubeIframeAPIReady() {}

        function onPlayerReady(event) {
            setVolume(document.getElementById('volume').value);
            updateMuteButton();
        }

        function onPlayerStateChange(event) {
            if (event.data == YT.PlayerState.PLAYING) {
                document.getElementById('visualizer').style.visibility = 'visible';
                startVisualizer();
                document.getElementById('playButton').classList.add('active');
                document.getElementById('stopButton').classList.remove('stop-active');
            } else if (event.data == YT.PlayerState.PAUSED) {
                document.getElementById('visualizer').style.visibility = 'hidden';
                stopVisualizer();
                document.getElementById('playButton').classList.remove('active');
                document.getElementById('stopButton').classList.add('stop-active');
            }
        }

        function startVisualizer() {
            var bars = document.querySelectorAll('#visualizer .bar');
            setInterval(() => {
                bars.forEach(bar => {
                    var height = Math.random() * 60 + 'px';
                    bar.style.height = height;
                });
            }, 100);
        }

        function stopVisualizer() {
            var bars = document.querySelectorAll('#visualizer .bar');
            bars.forEach(bar => bar.style.height = '0');
        }

        function playStream() {
            createPlayer();
            setActiveButton('playButton');
            document.getElementById('stopButton').classList.remove('stop-active');
        }

        function stopStream() {
            if (player) {
                player.stopVideo();
            }
            document.getElementById('visualizer').style.visibility = 'hidden';
            stopVisualizer();
            document.getElementById('stopButton').classList.add('stop-active');
            document.getElementById('playButton').classList.remove('active');
        }

        function muteUnmute() {
            isMuted = !isMuted;
            if (player) {
                player.mute();
                if (!isMuted) {
                    player.unMute();
                }
            }
            updateMuteButton();
        }

        function updateMuteButton() {
            var muteButton = document.getElementById('muteButton');
            if (isMuted) {
                muteButton.classList.add('muted');
                muteButton.textContent = 'Unmute';
            } else {
                muteButton.classList.remove('muted');
                muteButton.textContent = 'Mute';
            }
        }

        function setVolume(volume) {
            if (player) {
                player.setVolume(volume);
            }
        }

        function toggleDropdown() {
            var dropdown = document.getElementById('videoSelectDropdown');
            dropdown.style.display = dropdown.style.display === 'none' || dropdown.style.display === '' ? 'block' : 'none';
        }

        function changeVideo(videoId, category) {
            currentVideoId = videoId;
            currentCategory = category;
            document.getElementById('categoryLabel').textContent = 'Current radio: ' + currentCategory;
            if (player) {
                player.loadVideoById(videoId);
            } else {
                createPlayer();
            }
            var dropdown = document.getElementById('videoSelectDropdown');
            dropdown.style.display = 'none'; // Закрыть меню при переключении видео
        }

        function switchCategory(offset) {
            var categories = [
                { id: '8v_kKMaq5po', name: 'Phonk' },
                { id: 'sR-sbG98ldM', name: 'DnB / Electro' },
                { id: '0veWDx5beDs', name: 'Dark Techno' },
                { id: 'jfKfPfyJRdk', name: 'Lofi hip-hop' },
                { id: '3kgNy-kvFak', name: 'Retro 80s 90s' },
                { id: 'akHAQD3o1NA', name: 'GachiBass' }
            ];
            var currentIndex = categories.findIndex(cat => cat.id === currentVideoId);
            var newIndex = (currentIndex + offset + categories.length) % categories.length;
            changeVideo(categories[newIndex].id, categories[newIndex].name);
        }

        document.addEventListener('keydown', function(event) {
            if (event.altKey) {
                switch (event.key) {
                    case 'ArrowUp':
                        var volumeInput = document.getElementById('volume');
                        volumeInput.value = Math.min(100, parseInt(volumeInput.value) + 10);
                        setVolume(volumeInput.value);
                        break;
                    case 'ArrowDown':
                        var volumeInput = document.getElementById('volume');
                        volumeInput.value = Math.max(0, parseInt(volumeInput.value) - 10);
                        setVolume(volumeInput.value);
                        break;
                    case 'ArrowLeft':
                        switchCategory(-1);
                        break;
                    case 'ArrowRight':
                        switchCategory(1);
                        break;
                }
            }
        });
    </script>
</body>
</html>

"""

def create_webview_window():
    window = webview.create_window('YP-Radio', html=html_content, width=700, height=400, resizable=False)
    webview.start()

if __name__ == "__main__":
    create_webview_window()
