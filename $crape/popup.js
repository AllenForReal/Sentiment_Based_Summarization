document.addEventListener('DOMContentLoaded', function() {
    const analyzeButton = document.getElementById('analyzeButton');
    const classifierDropdown = document.getElementById('classifierDropdown');
    const modelDropdown = document.getElementById('modelDropdown');

    function updateUI(data) {
        document.getElementById('summaryResult').textContent = data.summary;
        
        let sentimentValue = parseFloat(data.sentiment);
        const degrees = 90 * sentimentValue + 90;
        const gaugeElement = document.querySelector('.gauge');
        const valueElement = gaugeElement.querySelector('.value');
        gaugeElement.style.setProperty('--rotation', `${degrees}deg`);
        valueElement.textContent = `${Math.round(sentimentValue * 100)}%`;
    }

    function fetchAndDisplayProductInfo(productId, classifier, model) {
        fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                productId: productId,
                classifier: classifier,
                model: model
            }),
        })                    
        .then(response => response.json())
        .then(data => {
            updateUI(data);

            const storageObject = {};
            storageObject[productId] = {
                sentiment: data.sentiment,
                summary: data.summary,
                classifier: classifier,
                model: model
            };
            chrome.storage.local.set(storageObject);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function attemptRestore(productId) {
        chrome.storage.local.get([productId], function(data) {
            if(data[productId]) {
                const storedData = data[productId];
                updateUI(storedData);
                classifierDropdown.value = storedData.classifier || 'defaultClassifier'; // Placeholder if not set
                modelDropdown.value = storedData.model || 'defaultModel'; // Placeholder if not set
            }
        });
    }

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        const tab = tabs[0];
        const url = new URL(tab.url);
        const domain = url.hostname;
        if (domain === "www.amazon.com") {
            const pathSegments = url.pathname.split('/');
            const productIdIndex = pathSegments.indexOf('dp') + 1;
            const productId = pathSegments[productIdIndex];
            attemptRestore(productId);

            analyzeButton.addEventListener('click', function() {
                const classifier = classifierDropdown.value;
                const model = modelDropdown.value;
                fetchAndDisplayProductInfo(productId, classifier, model);
            });
        } else {
            alert('This extension is only available for Amazon product pages.');
        }
    });
});