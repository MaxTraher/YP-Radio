import webview

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Live Stream Audio Player</title>
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
            right: 8px; /* Смещено влево на 3 пикселя */
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
            right: 8px; /* Смещено влево на 3 пикселя */
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
        }
        .button.active {
            background: #ee3a1f;
        }
        .button.muted {
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
            <div onclick="changeVideo('Cwq3AFyV044', 'Drum & Bass')">Drum & Bass</div>
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
                <input type="range" id="volume" min="0" max="100" value="100" onchange="setVolume(this.value)">
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
                    'mute': 0,
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

        function onPlayerReady(event) {}

        function onPlayerStateChange(event) {
            if (event.data == YT.PlayerState.PLAYING) {
                document.getElementById('visualizer').style.visibility = 'visible';
                startVisualizer();
            } else {
                document.getElementById('visualizer').style.visibility = 'hidden';
                stopVisualizer();
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
        }

        function stopStream() {
            if (player) {
                player.stopVideo();
                player.destroy();
                player = null;
            }
            document.getElementById('visualizer').style.visibility = 'hidden';
            stopVisualizer();
            setActiveButton('stopButton');
        }

        function muteUnmute() {
            if (player) {
                if (player.isMuted()) {
                    player.unMute();
                    isMuted = false;
                    document.getElementById('muteButton').classList.remove('muted');
                } else {
                    player.mute();
                    isMuted = true;
                    document.getElementById('muteButton').classList.add('muted');
                }
            }
        }

        function setVolume(value) {
            if (player) {
                var volume = value / 100;
                player.setVolume(volume * 100);
            }
        }

        function setActiveButton(buttonId) {
            document.querySelectorAll('#controls .button').forEach(button => {
                if (button.id !== 'muteButton') {
                    button.classList.remove('active');
                }
            });
            document.getElementById(buttonId).classList.add('active');
        }

        function toggleDropdown() {
            var dropdown = document.getElementById('videoSelectDropdown');
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        }

        function changeVideo(videoId, category) {
            currentVideoId = videoId;
            currentCategory = category;
            stopStream();
            playStream();
            document.getElementById('categoryLabel').textContent = `Current radio: ${category}`;
            toggleDropdown();
        }
    </script>
</body>
</html>
"""

def create_webview_window():
    webview_instance = webview.create_window('YouTube Live Stream Audio Player', html=html_content, width=700, height=400, resizable=False)
    webview.start()

if __name__ == "__main__":
    create_webview_window()
