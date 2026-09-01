document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const newsForm = document.getElementById('news-form');
    const newsText = document.getElementById('news-text');
    const resultsSection = document.getElementById('results-section');
    const loadingOverlay = document.getElementById('loading-overlay');
    const sourcesCard = document.getElementById('sources-card');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const clearButton = document.getElementById('clear-button');
    const sampleNewsButton = document.getElementById('sample-news-button');
    const fakeNewsSampleButton = document.getElementById('fake-news-sample-button');
    
    // Initialize dark mode based on user preference
    if (localStorage.getItem('darkMode') === 'darker') {
        document.body.classList.add('darker-mode');
        darkModeToggle.checked = true;
    } else if (localStorage.getItem('darkMode') === 'dark' || 
               window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }
    
    // Dark mode toggle
    darkModeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'dark');
            
            // Double-click to activate even darker mode
            document.body.addEventListener('dblclick', activateDarkerMode, { once: true });
            
            setTimeout(() => {
                alert('Tip: Double-click anywhere to activate even darker mode for enhanced readability');
            }, 1000);
        } else {
            document.body.classList.remove('dark-mode', 'darker-mode');
            localStorage.setItem('darkMode', 'light');
        }
    });
    
    function activateDarkerMode() {
        document.body.classList.remove('dark-mode');
        document.body.classList.add('darker-mode');
        localStorage.setItem('darkMode', 'darker');
    }
    
    // Form submission
    newsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const text = newsText.value.trim();
        if (!text) {
            alert('Please enter some news text to analyze');
            return;
        }
        
        // Show loading overlay
        loadingOverlay.classList.add('active');
        
        // Send request to backend
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ news_text: text })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading overlay
            loadingOverlay.classList.remove('active');
            
            console.log('Response data:', data);
            
            // Display results
            displayResults(data);
            
            // Show results section
            resultsSection.style.display = 'block';
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error:', error);
            loadingOverlay.classList.remove('active');
            alert('An error occurred while analyzing the news. Please try again.');
        });
    });
    
    function displayResults(data) {
        try {
            // Display credibility score and truth probability using Plotly gauges
            displayGauge('credibility-gauge', data.credibility_score, 'Credibility Score');
            displayGauge('truth-gauge', data.truth_probability, 'Truth Probability');
            
            // Display detailed metrics
            if (data.detailed_metrics) {
                displayMetrics(data.detailed_metrics);
            }
            
            // Display timeline
            if (data.timeline_data) {
                displayTimeline(data.timeline_data);
            }
            
            // Display source comparison if available (always show card, even for low cred to show warning)
            if (data.source_comparison !== undefined && data.source_comparison !== null) {
                displaySourceComparison(data.source_comparison, data.credibility_score);
            } else {
                // Fallback to show low-cred warning if field missing
                displaySourceComparison([], data.credibility_score || 0);
            }
            
            // Display AI insights if available
            if (data.ai_insights) {
                displayAIInsights(data.ai_insights);
            }
            
            // Show results section
            document.getElementById('results-section').style.display = 'block';
            
            // Scroll to results
            document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
        } catch (error) {
            console.error('Error displaying results:', error);
            showError('An error occurred while displaying the results. Please try again.');
        }
    }
    
    function displayGauge(gaugeId, value, title) {
        const gaugeElement = document.getElementById(gaugeId);
        if (!gaugeElement) {
            console.error(`Gauge element not found: ${gaugeId}`);
            return;
        }
        
        // Clear any existing content
        gaugeElement.innerHTML = '';
        
        // Ensure value is between 0 and 100
        const safeValue = Math.min(Math.max(parseFloat(value) || 0, 0), 100);
        
        // Update the value display
        const valueElement = document.querySelector(`#${gaugeId}-wrapper .gauge-value`);
        if (valueElement) {
            valueElement.textContent = `${safeValue.toFixed(1)}%`;
        }
        
        // Create gauge chart with Plotly
        Plotly.newPlot(gaugeId, [{
            domain: { x: [0, 1], y: [0, 1] },
            value: safeValue,
            title: { text: "" },
            type: "indicator",
            mode: "gauge",
            gauge: {
                axis: { 
                    range: [0, 100], 
                    visible: true, 
                    tickwidth: 1, 
                    tickcolor: "rgba(255,255,255,0.5)",
                    tickfont: { size: 10, color: "rgba(255,255,255,0.8)" }
                },
                bar: { color: getColorForScore(safeValue), thickness: 0.6 },
                bgcolor: "rgba(50, 50, 50, 0.8)",
                borderwidth: 0,
                bordercolor: "rgba(255,255,255,0.2)",
                steps: [
                    { range: [0, 40], color: "rgba(255, 23, 68, 0.3)" },
                    { range: [40, 60], color: "rgba(255, 145, 0, 0.3)" },
                    { range: [60, 80], color: "rgba(255, 234, 0, 0.3)" },
                    { range: [80, 100], color: "rgba(0, 230, 118, 0.3)" }
                ],
                threshold: {
                    line: { color: "white", width: 2 },
                    thickness: 0.75,
                    value: safeValue
                }
            }
        }], {
            paper_bgcolor: "rgba(0,0,0,0)",
            font: { color: document.body.classList.contains('dark-mode') ? "#e0e0e0" : "#333" },
            margin: { t: 0, b: 0, l: 0, r: 0 },
            height: 200,
            width: 200
        }, {
            responsive: true,
            displayModeBar: false
        });
    }
    
    function getColorForScore(score) {
        if (score >= 80) {
            return '#00e676'; // Green
        } else if (score >= 60) {
            return '#ffea00'; // Yellow
        } else if (score >= 40) {
            return '#ff9100'; // Orange
        } else {
            return '#ff1744'; // Red
        }
    }
    
    function displayTimeline(timelineData) {
        try {
            const timelineElement = document.getElementById('timeline-chart');
            
            if (!timelineElement) {
                console.error('Timeline element not found');
                return;
            }
            
            if (typeof Plotly === 'undefined') {
                console.error('Plotly library not loaded');
                return;
            }

            // Clean up previous plot to avoid duplicate traces (fixes double-line artifact)
            try { Plotly.purge('timeline-chart'); } catch(e) {}

            // Remove previous resize handler if exists (prevent accumulation)
            if (window._timelineResizeHandler) {
                window.removeEventListener('resize', window._timelineResizeHandler);
                window._timelineResizeHandler = null;
            }
            
            // Use real Date objects for X to avoid duplicate HH:MM categorical bug (48h -> duplicate labels)
            // Backend now sends ISO timestamps; fallback handles old "YYYY-MM-DD HH:MM:SS" format
            const xValues = timelineData.map(point => new Date(point.timestamp));
            const yValues = timelineData.map(point => point.score);

            // Compute dynamic Y range for better visual variation while keeping 0-100 bounds
            const minScore = Math.min(...yValues);
            const maxScore = Math.max(...yValues);
            const pad = 8;
            const yMin = Math.max(0, Math.floor(minScore - pad));
            const yMax = Math.min(100, Math.ceil(maxScore + pad));
            // If variation is still tiny (<6), force wider window around base score
            const finalYMin = (yMax - yMin < 12) ? Math.max(0, Math.round(yValues[yValues.length-1] - 12)) : yMin;
            const finalYMax = (yMax - yMin < 12) ? Math.min(100, Math.round(yValues[yValues.length-1] + 12)) : yMax;

            const layout = {
                title: {
                    text: 'Credibility Score Over Time',
                    font: {
                        size: 16,
                        color: '#e0e0e0'
                    }
                },
                paper_bgcolor: 'rgba(30, 34, 42, 0.0)',
                plot_bgcolor: 'rgba(30, 34, 42, 0.5)',
                font: {
                    color: '#e0e0e0'
                },
                xaxis: {
                    title: 'Time',
                    type: 'date',
                    tickformat: '%H:%M<br>%m/%d',
                    hoverformat: '%Y-%m-%d %H:%M',
                    showgrid: true,
                    gridcolor: 'rgba(80, 90, 120, 0.3)',
                    tickfont: { size: 10 },
                    tickangle: -20
                },
                yaxis: {
                    title: 'Credibility Score (%)',
                    range: [finalYMin, finalYMax],
                    showgrid: true,
                    gridcolor: 'rgba(80, 90, 120, 0.3)',
                    tickfont: { size: 10 },
                    fixedrange: false
                },
                margin: { l: 55, r: 20, t: 50, b: 65 },
                autosize: true,
                hovermode: 'x unified',
                height: null,
                width: null
            };
            
            const config = {
                responsive: true,
                displayModeBar: false,
                scrollZoom: false,
                modeBarButtonsToRemove: ['lasso2d', 'select2d']
            };
            
            // Single trace with spline and filled area - no duplicate
            Plotly.newPlot('timeline-chart', [{
                x: xValues,
                y: yValues,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Credibility',
                line: {
                    color: '#4a6bff',
                    width: 3,
                    shape: 'spline',
                    smoothing: 0.8
                },
                marker: {
                    color: '#4a6bff',
                    size: 6,
                    line: { color: 'white', width: 1 }
                },
                fill: 'tozeroy',
                fillcolor: 'rgba(74, 107, 255, 0.18)',
                hovertemplate: '%{x|%Y-%m-%d %H:%M}<br>Score: %{y:.1f}%<extra></extra>'
            }], layout, config);
            
            const resizeChart = () => {
                const container = timelineElement.parentElement;
                if (!container) return;
                const width = container.clientWidth;
                const height = container.clientHeight;
                // Use Plots.resize for proper responsive handling instead of relayout width/height
                try { Plotly.Plots.resize('timeline-chart'); } catch(e) {
                    try { Plotly.relayout('timeline-chart', { width: width, height: height }); } catch(e2) {}
                }
            };
            
            window._timelineResizeHandler = resizeChart;
            setTimeout(resizeChart, 120);
            window.addEventListener('resize', resizeChart);
        } catch (error) {
            console.error('Error displaying timeline:', error);
        }
    }
    
    function displayMetrics(metrics) {
        try {
            if (!metrics) {
                console.error('No metrics data provided');
                return;
            }
            
            // Display sentiment score
            const sentimentBar = document.getElementById('sentiment-bar');
            const sentimentValue = document.getElementById('sentiment-value');
            
            if (sentimentBar && sentimentValue && metrics.sentiment_score !== undefined) {
                const sentimentScore = parseFloat(metrics.sentiment_score).toFixed(1);
                
                // Normalize sentiment score from -100..100 to 0..100 for display
                const normalizedSentiment = (parseFloat(sentimentScore) + 100) / 2;
                sentimentBar.style.width = normalizedSentiment + '%';
                sentimentValue.textContent = sentimentScore;
                
                // Color based on sentiment
                if (sentimentScore > 50) {
                    sentimentBar.style.background = 'linear-gradient(90deg, #4a6bff, #00e676)';
                } else if (sentimentScore > 0) {
                    sentimentBar.style.background = 'linear-gradient(90deg, #4a6bff, #ffea00)';
                } else if (sentimentScore > -50) {
                    sentimentBar.style.background = 'linear-gradient(90deg, #ffea00, #ff9100)';
                } else {
                    sentimentBar.style.background = 'linear-gradient(90deg, #ff9100, #ff1744)';
                }
            } else {
                console.error('Sentiment score elements not found or data missing');
            }
            
            // Display bias score
            const biasBar = document.getElementById('bias-bar');
            const biasValue = document.getElementById('bias-value');
            
            if (biasBar && biasValue && metrics.bias_score !== undefined) {
                const biasScore = parseFloat(metrics.bias_score).toFixed(1);
                
                biasBar.style.width = biasScore + '%';
                biasValue.textContent = biasScore;
                
                // Color based on bias (higher is worse)
                if (biasScore < 30) {
                    biasBar.style.background = 'linear-gradient(90deg, #4a6bff, #00e676)';
                } else if (biasScore < 50) {
                    biasBar.style.background = 'linear-gradient(90deg, #4a6bff, #ffea00)';
                } else if (biasScore < 70) {
                    biasBar.style.background = 'linear-gradient(90deg, #ffea00, #ff9100)';
                } else {
                    biasBar.style.background = 'linear-gradient(90deg, #ff9100, #ff1744)';
                }
            } else {
                console.error('Bias score elements not found or data missing');
            }
            
            // Display fact check confidence
            const factCheckBar = document.getElementById('fact-check-bar');
            const factCheckValue = document.getElementById('fact-check-value');
            
            if (factCheckBar && factCheckValue && metrics.fact_check_confidence !== undefined) {
                const factCheckScore = parseFloat(metrics.fact_check_confidence).toFixed(1);
                
                factCheckBar.style.width = factCheckScore + '%';
                factCheckValue.textContent = factCheckScore;
                
                // Color based on confidence (higher is better)
                if (factCheckScore >= 80) {
                    factCheckBar.style.background = 'linear-gradient(90deg, #4a6bff, #00e676)';
                } else if (factCheckScore >= 60) {
                    factCheckBar.style.background = 'linear-gradient(90deg, #4a6bff, #ffea00)';
                } else if (factCheckScore >= 40) {
                    factCheckBar.style.background = 'linear-gradient(90deg, #ffea00, #ff9100)';
                } else {
                    factCheckBar.style.background = 'linear-gradient(90deg, #ff9100, #ff1744)';
                }
            } else {
                console.error('Fact check elements not found or data missing');
            }
            
            // Display manipulative language score
            const manipulativeBar = document.getElementById('manipulative-bar');
            const manipulativeValue = document.getElementById('manipulative-value');
            
            if (manipulativeBar && manipulativeValue && metrics.manipulative_language !== undefined) {
                const manipulativeScore = parseFloat(metrics.manipulative_language).toFixed(1);
                
                manipulativeBar.style.width = manipulativeScore + '%';
                manipulativeValue.textContent = manipulativeScore;
                
                // Color based on manipulative language (higher is worse)
                if (manipulativeScore < 30) {
                    manipulativeBar.style.background = 'linear-gradient(90deg, #4a6bff, #00e676)';
                } else if (manipulativeScore < 50) {
                    manipulativeBar.style.background = 'linear-gradient(90deg, #4a6bff, #ffea00)';
                } else if (manipulativeScore < 70) {
                    manipulativeBar.style.background = 'linear-gradient(90deg, #ffea00, #ff9100)';
                } else {
                    manipulativeBar.style.background = 'linear-gradient(90deg, #ff9100, #ff1744)';
                }
            } else {
                console.error('Manipulative language elements not found or data missing');
            }
            
            // Display source reliability
            const sourceBar = document.getElementById('source-bar');
            const sourceValue = document.getElementById('source-value');
            
            if (sourceBar && sourceValue && metrics.source_reliability !== undefined) {
                const sourceScore = parseFloat(metrics.source_reliability).toFixed(1);
                
                sourceBar.style.width = sourceScore + '%';
                sourceValue.textContent = sourceScore;
                
                // Color based on source reliability (higher is better)
                if (sourceScore >= 80) {
                    sourceBar.style.background = 'linear-gradient(90deg, #4a6bff, #00e676)';
                } else if (sourceScore >= 60) {
                    sourceBar.style.background = 'linear-gradient(90deg, #4a6bff, #ffea00)';
                } else if (sourceScore >= 40) {
                    sourceBar.style.background = 'linear-gradient(90deg, #ffea00, #ff9100)';
                } else {
                    sourceBar.style.background = 'linear-gradient(90deg, #ff9100, #ff1744)';
                }
            } else {
                console.error('Source reliability elements not found or data missing');
            }
        } catch (error) {
            console.error('Error displaying metrics:', error);
        }
    }
    
    function displaySourceComparison(sourceComparison, credibilityScore) {
        try {
            const sourcesCard = document.getElementById('sources-card');
            const sourcesContainer = document.getElementById('sources-container');
            const regionValue = document.getElementById('region-value');
            const confidenceValue = document.getElementById('overall-confidence');
            
            if (!sourcesContainer || !sourcesCard) {
                console.error('Sources container/card not found');
                return;
            }
            
            // Clear previous content
            sourcesContainer.innerHTML = '';
            sourcesCard.style.display = 'block';

            // Normalize input: backend returns {region, articles} for credible, [] for low cred
            let articles = [];
            let region = 'us';
            let isLowCredibility = false;

            if (!sourceComparison) {
                isLowCredibility = true;
            } else if (Array.isArray(sourceComparison)) {
                // Old low-cred path returns [] or array of sources (rare)
                if (sourceComparison.length === 0) {
                    isLowCredibility = true;
                } else {
                    // If it's array of articles directly
                    articles = sourceComparison;
                    // try to infer region from first item or default
                    region = sourceComparison[0].region || 'us';
                }
            } else if (typeof sourceComparison === 'object') {
                // Expected {region, articles}
                region = sourceComparison.region || 'us';
                articles = sourceComparison.articles || [];
                if (!articles || articles.length === 0) {
                    isLowCredibility = true;
                }
            }

            // Update header info
            if (regionValue) regionValue.textContent = region.toUpperCase();
            if (confidenceValue) {
                const score = credibilityScore !== undefined ? credibilityScore : '--';
                confidenceValue.textContent = typeof score === 'number' ? score.toFixed(1) + '%' : score;
            }

            if (isLowCredibility) {
                const noSourcesMessage = document.createElement('div');
                noSourcesMessage.className = 'no-sources-message';
                noSourcesMessage.innerHTML = `
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span>Source comparison is not available for content with low credibility (below 80%). 
                        The system has detected potentially misleading information in this content.</span>
                    </div>
                `;
                sourcesContainer.appendChild(noSourcesMessage);
                return;
            }
            
            // Display the articles - backend article shape: {source, title, summary, date, url, bias}
            articles.forEach(article => {
                if (!article) return;
                
                try {
                    const sourceElement = document.createElement('div');
                    sourceElement.className = 'source-item';
                    
                    const sourceName = article.source || article.name || 'Unnamed Source';
                    const title = article.title || 'No title';
                    const summary = article.summary || article.description || 'No summary available';
                    const date = article.date || '';
                    const url = article.url || '#';
                    const bias = article.bias || 'unknown';
                    const biasClass = getBiasClass(bias);
                    
                    sourceElement.innerHTML = `
                        <div class="source-name">${sourceName} <span class="source-confidence-value ${biasClass}" style="float:right; font-size:0.8em;">${bias}</span></div>
                        <div class="source-title">${title}</div>
                        <div class="source-summary">${summary}</div>
                        <div class="source-confidence">
                            <span class="source-confidence-label"><i class="fas fa-calendar"></i> ${date}</span>
                            <span class="source-confidence-label"><i class="fas fa-balance-scale"></i> ${bias}</span>
                        </div>
                        <div class="source-link"><a href="${url}" target="_blank">Read full coverage <i class="fas fa-external-link-alt"></i></a></div>
                    `;
                    
                    sourcesContainer.appendChild(sourceElement);
                } catch (sourceError) {
                    console.warn('Error displaying individual source:', sourceError);
                }
            });
        } catch (error) {
            console.error('Error displaying source comparison:', error);
            
            try {
                const sourcesCard = document.getElementById('sources-card');
                const sourcesContainer = document.getElementById('sources-container');
                
                if (sourcesContainer) {
                    sourcesContainer.innerHTML = `
                        <div class="alert alert-danger">
                            <i class="fas fa-exclamation-circle"></i>
                            <span>There was an error displaying source comparisons. Please try again.</span>
                        </div>
                    `;
                    if (sourcesCard) sourcesCard.style.display = 'block';
                }
            } catch (fallbackError) {
                console.error('Error in fallback display:', fallbackError);
            }
        }
    }

    function getBiasClass(bias) {
        if (!bias) return '';
        const b = bias.toLowerCase();
        if (b.includes('center-left') || b.includes('center-right')) return 'bias-center';
        if (b === 'center') return 'bias-center';
        if (b.includes('left')) return 'bias-left';
        if (b.includes('right')) return 'bias-right';
        return '';
    }

    function getReliabilityClass(reliability) {
        if (!reliability || reliability === 'Unknown') return '';
        const r = String(reliability).toLowerCase();
        if (r.includes('high') || r === 'center' || r.includes('reliable')) return 'high';
        if (r.includes('medium')) return 'medium';
        if (r.includes('low')) return 'low';
        return '';
    }

    function showError(msg) {
        console.error(msg);
        // Show as alert if no better UI
        const el = document.getElementById('sources-container') || document.body;
        if (el) {
            const div = document.createElement('div');
            div.className = 'alert alert-danger';
            div.style.cssText = 'background:rgba(255,23,68,0.2); border-left:4px solid #ff1744; padding:12px; margin:15px; border-radius:8px; color:#e0e0e0;';
            div.innerHTML = '<i class="fas fa-exclamation-circle"></i> ' + msg;
            // Prepend to results section if possible
            const rs = document.getElementById('results-section');
            if (rs && rs.style.display !== 'none') {
                rs.prepend(div);
                setTimeout(()=>div.remove(), 5000);
            } else {
                alert(msg);
            }
        }
    }
    
    function displayAIInsights(insights) {
        const insightsCard = document.getElementById('ai-insights-card');
        if (!insightsCard) {
            console.error('AI insights card not found');
            return;
        }
        
        // Show the card
        insightsCard.style.display = 'block';
        
        // Get the container for insights
        const insightsContainer = document.getElementById('ai-insights-container');
        if (!insightsContainer) {
            console.error('AI insights container not found');
            return;
        }
        
        // Clear previous insights
        insightsContainer.innerHTML = '';
        
        // Create pattern matches section if there are matches
        if (insights.pattern_matches && insights.pattern_matches.length > 0) {
            const patternSection = document.createElement('div');
            patternSection.className = 'insights-section';
            
            const patternTitle = document.createElement('h4');
            patternTitle.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Suspicious Patterns Detected';
            patternTitle.className = 'insights-title';
            patternSection.appendChild(patternTitle);
            
            const patternList = document.createElement('ul');
            patternList.className = 'insights-list';
            
            insights.pattern_matches.forEach(pattern => {
                const patternItem = document.createElement('li');
                // Clean up the pattern for display
                const displayPattern = pattern.replace(/\(\?i\)/g, '')
                                             .replace(/[\\(\\)]/g, '')
                                             .replace(/\.\{[0-9,]+\}/g, ' ')
                                             .replace(/\|/g, ' or ');
                patternItem.textContent = displayPattern;
                patternList.appendChild(patternItem);
            });
            
            patternSection.appendChild(patternList);
            insightsContainer.appendChild(patternSection);
        }
        
        // Create scientific impossibilities section if there are any
        if (insights.scientific_impossibilities && insights.scientific_impossibilities.length > 0) {
            const impossibilitySection = document.createElement('div');
            impossibilitySection.className = 'insights-section';
            
            const impossibilityTitle = document.createElement('h4');
            impossibilityTitle.innerHTML = '<i class="fas fa-flask"></i> Scientific Impossibilities';
            impossibilityTitle.className = 'insights-title';
            impossibilitySection.appendChild(impossibilityTitle);
            
            const impossibilityList = document.createElement('ul');
            impossibilityList.className = 'insights-list';
            
            insights.scientific_impossibilities.forEach(impossibility => {
                const impossibilityItem = document.createElement('li');
                impossibilityItem.textContent = impossibility;
                impossibilityList.appendChild(impossibilityItem);
            });
            
            impossibilitySection.appendChild(impossibilityList);
            insightsContainer.appendChild(impossibilitySection);
        }
        
        // Add model confidence
        if (insights.model_confidence !== undefined) {
            const confidenceSection = document.createElement('div');
            confidenceSection.className = 'insights-section';
            
            const confidenceTitle = document.createElement('h4');
            confidenceTitle.innerHTML = '<i class="fas fa-brain"></i> AI Model Confidence';
            confidenceTitle.className = 'insights-title';
            confidenceSection.appendChild(confidenceTitle);
            
            const confidenceValue = document.createElement('div');
            confidenceValue.className = 'model-confidence';
            confidenceValue.textContent = `${insights.model_confidence}%`;
            confidenceSection.appendChild(confidenceValue);
            
            insightsContainer.appendChild(confidenceSection);
        }
        
        // Add a conclusion based on the insights
        const conclusionSection = document.createElement('div');
        conclusionSection.className = 'insights-section conclusion';
        
        const conclusionTitle = document.createElement('h4');
        conclusionTitle.innerHTML = '<i class="fas fa-check-circle"></i> AI Analysis Conclusion';
        conclusionTitle.className = 'insights-title';
        conclusionSection.appendChild(conclusionTitle);
        
        const conclusionText = document.createElement('p');
        if (insights.pattern_matches.length > 0 || insights.scientific_impossibilities.length > 0) {
            conclusionText.textContent = 'This content contains elements commonly found in fake news articles. Be skeptical and verify with trusted sources.';
        } else {
            conclusionText.textContent = 'No obvious fake news patterns detected, but always verify information with trusted sources.';
        }
        conclusionSection.appendChild(conclusionText);
        
        insightsContainer.appendChild(conclusionSection);
    }
    
    // Clear button functionality
    clearButton.addEventListener('click', function() {
        newsText.value = '';
        newsText.focus();
        
        // Hide results section if it's visible
        if (resultsSection.style.display !== 'none') {
            resultsSection.style.display = 'none';
        }
    });
    
    // Sample news button functionality
    sampleNewsButton.addEventListener('click', function() {
        newsText.value = `NASA's Perseverance rover has collected promising samples from Mars that show evidence of ancient microbial life, according to scientists at the Jet Propulsion Laboratory. The samples contain organic compounds and minerals typically formed in the presence of living organisms. While researchers caution that more analysis is needed before drawing definitive conclusions, the findings represent a significant step in understanding whether life ever existed on the Red Planet. The samples will be returned to Earth by a future mission for more detailed laboratory examination.`;
        
        // Automatically submit the form
        const submitEvent = new Event('submit', { cancelable: true });
        newsForm.dispatchEvent(submitEvent);
    });

    // Fake news sample button functionality
    fakeNewsSampleButton.addEventListener('click', function() {
        newsText.value = `NASA Confirms the Moon is Composed Entirely of Cheese
NASA scientists have allegedly made a groundbreaking discovery, claiming that the Moon is not made of rock and dust but is, in fact, composed entirely of cheese. This revelation is said to have come after an extensive lunar mission that retrieved samples proving the dairy-based composition. The space agency is now reportedly planning an international collaboration to begin commercial cheese extraction from the Moon.`;
        
        // Automatically submit the form
        const submitEvent = new Event('submit', { cancelable: true });
        newsForm.dispatchEvent(submitEvent);
    });
});
