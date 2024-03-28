document.addEventListener('DOMContentLoaded', function() {
    var analyzeButton = document.getElementById('analyzeButton');

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        var tab = tabs[0];
        var url = new URL(tab.url);
        var domain = url.hostname;
        if (domain === "www.amazon.com") {
            var pathSegments = url.pathname.split('/');
            var productIdIndex = pathSegments.indexOf('dp') + 1;
            var productId = pathSegments[productIdIndex];
            
            chrome.storage.local.get([productId], function(data) {
                if(data[productId]) {
                    var storedData = data[productId];
                    if(storedData.sentiment && storedData.summary) {
                        document.getElementById('summaryResult').textContent = storedData.summary;

                        const degrees = 90 * storedData.sentiment + 90; 
                        const gaugeElement = document.querySelector('.gauge');
                        const valueElement = gaugeElement.querySelector('.value');
                        gaugeElement.style.setProperty('--rotation', `${degrees}deg`);
                        valueElement.textContent = `${Math.round(storedData.sentiment * 100)}%`;
                    }
                }
            });
        }
    });

    analyzeButton.addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            var tab = tabs[0];
            var url = new URL(tab.url);
            var domain = url.hostname;
            if(domain === "www.amazon.com") {
                var pathSegments = url.pathname.split('/');
                var productIdIndex = pathSegments.indexOf('dp') + 1;
                var productId = pathSegments[productIdIndex];
                if(productId) {
                    fetch('http://127.0.0.1:5000/analyze', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ productId: productId }),
                    })                    
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('summaryResult').textContent = data.summary;

                        let sentimentValue = parseFloat(data.sentiment);
                        if (sentimentValue > 0) {
                            sentimentValue = Math.min(sentimentValue*10, 1);
                        } else if (sentimentValue < 0) {
                            sentimentValue = Math.max(sentimentValue*10, -1);
                        }
                        
                        const degrees = 90 * sentimentValue + 90;
                        const gaugeElement = document.querySelector('.gauge');
                        const valueElement = gaugeElement.querySelector('.value');
                        gaugeElement.style.setProperty('--rotation', `${degrees}deg`);
                        valueElement.textContent = `${Math.round(sentimentValue * 100)}%`;
                        gaugeElement.style.setProperty('--background-position', `${degrees*(5/11)}%`);

                        var storageObject = {};
                        storageObject[productId] = { 'sentiment': sentimentValue, 'summary': data.summary };
                        chrome.storage.local.set(storageObject);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                }
            } else {
                alert('This extension is only available for Amazon product pages.');
            }
        });
    }, false);
}, false);