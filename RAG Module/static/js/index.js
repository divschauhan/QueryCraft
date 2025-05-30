// // $(function() {
// //     var synth = window.speechSynthesis;
// //     var msg = new SpeechSynthesisUtterance();
// //     var voices = synth.getVoices();
// //     msg.voice = voices[0];
// //     msg.rate = 1;
// //     msg.pitch = 1;

// //     function appendMessage(message, isUser) {
// //         var messageClass = isUser ? 'user-message' : 'bot-message';
// //         //var logoHTML = isUser ? '' : '<div class="bot-logo"><img src="../static/robo.png" alt="AgriGenius Logo"></div>';
// //         //var userImageHTML = isUser ? '<div class="user-image"><img src="../static/user.png" alt="User"></div>' : '';
// //         var logoHTML = isUser ? '' : '';
// //         var userImageHTML = isUser ? '' : '';
       
// //         var messageElement = $('<div class="message-container ' + (isUser ? 'user-container' : 'bot-container') + '">' + 
// //                             logoHTML + 
// //                             '<div class="message ' + messageClass + '"></div>' +
// //                             userImageHTML +
// //                            '</div>');
// //         $('.chat-messages').append(messageElement);

// //         if (isUser) {
// //             messageElement.find('.message').text(message);
// //         } else {
// //             typeMessage(message, messageElement.find('.message'));
// //         }

// //         $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
// //     }

// //     function typeMessage(message, element, speed = 15) {
// //         let i = 0;
// //         element.html('');
// //         const typingInterval = setInterval(() => {
// //             if (i < message.length) {
// //                 element.html(element.html() + message.charAt(i));
// //                 i++;
// //             } else {
// //                 clearInterval(typingInterval);
// //             }
// //             $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
// //         }, speed);
// //     }

// //     function showTypingIndicator() {
// //         var typingIndicator = $('<div class="typing-indicator bot-message"><span></span><span></span><span></span></div>');
// //         $('.chat-messages').append(typingIndicator);
// //         $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
// //     }

// //     function removeTypingIndicator() {
// //         $('.typing-indicator').remove();
// //     }

// //     $('#chatbot-form-btn').click(function(e) {
// //         e.preventDefault();
// //         sendMessage();
// //     });

// //     $('#messageText').keypress(function(e) {
// //         if (e.which == 13) {
// //             e.preventDefault();
// //             sendMessage();
// //         }
// //     });

// //     var isProcessing = false;

// //     function disableInput() {
// //         $('#messageText').prop('disabled', true);
// //         $('#chatbot-form-btn').prop('disabled', true);
// //         $('#chatbot-form-btn-voice').prop('disabled', true);
// //     }

// //     function enableInput() {
// //         $('#messageText').prop('disabled', false);
// //         $('#chatbot-form-btn').prop('disabled', false);
// //         $('#chatbot-form-btn-voice').prop('disabled', false);
// //     }
    
// //     function sendMessage() {
// //         var message = $('#messageText').val().trim();
// //         if (message && !isProcessing) {
// //             isProcessing = true;
// //             disableInput();
            
// //             appendMessage(message, true);
// //             $('#messageText').val('');
// //             showTypingIndicator();

// //             $.ajax({
// //                 type: "POST",
// //                 url: "/ask", // Backend route to handle the request
// //                 data: { messageText: message },// User's input is sent as 'messageText'
// //                 success: function(response) {
// //                     removeTypingIndicator();
// //                     if (response.error) {
// //                         appendMessage("Error: " + response.error, false);
// //                     } else {
// //                         var answer = response.answer;
// //                         appendMessage(answer, false);

// //                         if ($('#voiceReadingCheckbox').is(':checked')) {
// //                             msg.text = answer;
// //                             synth.speak(msg);
// //                         }
// //                     }
// //                     isProcessing = false;
// //                     enableInput();
// //                 },
// //                 error: function(jqXHR, textStatus, errorThrown) {
// //                     removeTypingIndicator();
// //                     console.log(errorThrown);
// //                     appendMessage("Sorry, there was an error processing your request. Please try again later.", false);
// //                     isProcessing = false;
// //                     enableInput();
// //                 }
// //             });
// //         }
// //     }

// //     var welcomeMessage = "🌱🌾 Welcome to KrishiAI !! 🌾🌱 How can I assist you today?";

// //     $('#chatbot-form-btn-clear').click(function(e) {
// //         e.preventDefault();
// //         $('.chat-messages').empty();
// //         appendMessage(welcomeMessage, false);
// //     });

// //     $('#chatbot-form-btn-voice').click(function(e) {
// //         e.preventDefault();

// //         if ('webkitSpeechRecognition' in window && !isProcessing) {
// //             var recognition = new webkitSpeechRecognition();
// //             recognition.lang = 'en-US';
// //             recognition.interimResults = false;
// //             recognition.maxAlternatives = 1;

// //             recognition.start();

// //             recognition.onresult = function(event) {
// //                 var speechResult = event.results[0][0].transcript;
// //                 $('#messageText').val(speechResult);
// //                 sendMessage();
// //             };

// //             recognition.onerror = function(event) {
// //                 console.error('Speech recognition error:', event.error);
// //             };
// //         } else {
// //             console.log('Web Speech API is not supported in this browser or processing is in progress');
// //         }
// //     });

// //     $('#voiceReadingCheckbox').change(function() {
// //         if (!$(this).is(':checked')) {
// //             synth.cancel();
// //         }
// //     });

// //     setTimeout(function() {
// //         appendMessage(welcomeMessage, false);
// //     }, 500);
// // });




// //----------------------------------------------------------------------------------------------------
// //-------------------------------------------------------------------------------------------
// //----------------------------------------------------------------------------------------------------
// //-------------------------------------------------------------------------------------------

// $(function() {
//     var synth = window.speechSynthesis;
//     var msg = new SpeechSynthesisUtterance();

//     function setVoice() {
//         var voices = synth.getVoices();
//         var selectedVoice = voices.find(v => v.name === "Microsoft Heera" && v.lang === "en-IN");

//         // Use Microsoft Heera if found, otherwise use the default voice
//         msg.voice = selectedVoice || voices[0];

//         msg.rate = 1;   // Normal speed
//         msg.pitch = 1;  // Normal pitch

//     }



//     var isPaused = false;
//     var typingInterval;

//     function appendMessage(message, isUser) {
//         var messageClass = isUser ? 'user-message' : 'bot-message';
//         var logoHTML = isUser ? '' : '';
//         var userImageHTML = isUser ? '' : '';

//         var messageElement = $('<div class="message-container ' + (isUser ? 'user-container' : 'bot-container') + '">' + 
//                             logoHTML + 
//                             '<div class="message ' + messageClass + '"></div>' +
//                             userImageHTML +
//                            '</div>');
//         $('.chat-messages').append(messageElement);

//         if (isUser) {
//             messageElement.find('.message').text(message);
//         } else {
//             typeMessage(message, messageElement.find('.message'));
//         }

//         $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
//     }

//     function typeMessage(message, element, speed = 15) {
//         let i = 0;
//         isPaused = false; // Reset pause state
//         element.html('');
//         typingInterval = setInterval(() => {
//             if (i < message.length && !isPaused) {
//                 element.html(element.html() + message.charAt(i));
//                 i++;
//             } else {
//                 clearInterval(typingInterval);
//             }
//             $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
//         }, speed);
//     }

//     function stopTyping() {
//         isPaused = true;
//         clearInterval(typingInterval);
//     }

//     function showTypingIndicator() {
//         var typingIndicator = $('<div class="typing-indicator bot-message"><span></span><span></span><span></span></div>');
//         $('.chat-messages').append(typingIndicator);
//         $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
//     }

//     function removeTypingIndicator() {
//         $('.typing-indicator').remove();
//     }

//     $('#chatbot-form-btn').click(function(e) {
//         e.preventDefault();
//         sendMessage();
//     });

//     $('#messageText').keypress(function(e) {
//         if (e.which == 13) {
//             e.preventDefault();
//             sendMessage();
//         }
//     });

//     var isProcessing = false;

//     function disableInput() {
//         $('#messageText, #chatbot-form-btn, #chatbot-form-btn-voice, #chatbot-form-btn-pause').prop('disabled', true);
//     }

//     function enableInput() {
//         $('#messageText, #chatbot-form-btn, #chatbot-form-btn-voice, #chatbot-form-btn-pause').prop('disabled', false);
//     }

//     function sendMessage() {
//         var message = $('#messageText').val().trim();
//         if (message && !isProcessing) {
//             isProcessing = true;
//             disableInput();

//             appendMessage(message, true);
//             $('#messageText').val('');
//             showTypingIndicator();

//             $.ajax({
//                 type: "POST",
//                 url: "/ask",
//                 data: { messageText: message },
//                 success: function(response) {
//                     removeTypingIndicator();
//                     if (response.error) {
//                         appendMessage("Error: " + response.error, false);
//                     } else {
//                         var answer = response.answer;
//                         appendMessage(answer, false);

//                         if ($('#voiceReadingCheckbox').is(':checked')) {
//                             msg.text = answer;
//                             synth.speak(msg);
//                         }
//                     }
//                     isProcessing = false;
//                     enableInput();
//                 },
//                 error: function(jqXHR, textStatus, errorThrown) {
//                     removeTypingIndicator();
//                     console.log(errorThrown);
//                     appendMessage("Sorry, there was an error processing your request. Please try again later.", false);
//                     isProcessing = false;
//                     enableInput();
//                 }
//             });
//         }
//     }

//     var welcomeMessage = "🌱🌾 Welcome to KrishiAI !! 🌾🌱 How can I assist you today?";

//     $('#chatbot-form-btn-clear').click(function(e) {
//         e.preventDefault();
//         $('.chat-messages').empty();
//         appendMessage(welcomeMessage, false);
//     });

//     $('#chatbot-form-btn-voice').click(function(e) {
//         e.preventDefault();

//         if ('webkitSpeechRecognition' in window && !isProcessing) {
//             var recognition = new webkitSpeechRecognition();
//             recognition.lang = 'en-US';
//             recognition.interimResults = false;
//             recognition.maxAlternatives = 1;

//             recognition.start();

//             recognition.onresult = function(event) {
//                 var speechResult = event.results[0][0].transcript;
//                 $('#messageText').val(speechResult);
//                 sendMessage();
//             };

//             recognition.onerror = function(event) {
//                 console.error('Speech recognition error:', event.error);
//             };
//         } else {
//             console.log('Web Speech API is not supported in this browser or processing is in progress');
//         }
//     });

//     $('#voiceReadingCheckbox').change(function() {
//         if (!$(this).is(':checked')) {
//             synth.cancel();
//         }
//     });

//     // PAUSE BUTTON FUNCTIONALITY
//     $('#chatbot-form-btn-pause').click(function() {
//         stopTyping(); // Stops text from typing
//         synth.cancel(); // Stops voice reading
//     });

//     setTimeout(function() {
//         appendMessage(welcomeMessage, false);
//     }, 500);
// });



$(function() {
    var synth = window.speechSynthesis;
    var msg = new SpeechSynthesisUtterance();

    function setVoice() {
        var voices = synth.getVoices();
        var selectedVoice = voices.find(v => v.name === "Microsoft Heera" && v.lang === "en-IN");

        // Use Microsoft Heera if found, otherwise use the default voice
        msg.voice = selectedVoice || voices[0];

        msg.rate = 1;   // Normal speed
        msg.pitch = 1;  // Normal pitch
    }

    var isPaused = false;
    var typingInterval;

    function appendMessage(message, isUser, imageUrl = null) {
        var messageClass = isUser ? 'user-message' : 'bot-message';
        var logoHTML = isUser ? '' : '';
        var userImageHTML = isUser ? '' : '';

        var messageElement = $('<div class="message-container ' + (isUser ? 'user-container' : 'bot-container') + '">' + 
                            logoHTML + 
                            '<div class="message ' + messageClass + '"></div>' +
                            userImageHTML +
                           '</div>');
        $('.chat-messages').append(messageElement);

        if (isUser) {
            if (imageUrl) {
                // If there's an image, create an image message
                var imgElement = $('<div class="image-message"><img src="' + imageUrl + '" alt="Uploaded plant image"><div>Analyzing this plant image...</div></div>');
                messageElement.find('.message').append(imgElement);
            } else {
                messageElement.find('.message').text(message);
            }
        } else {
            typeMessage(message, messageElement.find('.message'));
        }

        $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
    }

    function typeMessage(message, element, speed = 15) {
        let i = 0;
        isPaused = false; // Reset pause state
        element.html('');
        typingInterval = setInterval(() => {
            if (i < message.length && !isPaused) {
                element.html(element.html() + message.charAt(i));
                i++;
            } else if (i >= message.length) {
                clearInterval(typingInterval);
            }
            $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
        }, speed);
    }

    function stopTyping() {
        isPaused = true;
        clearInterval(typingInterval);
    }

    function showTypingIndicator() {
        var typingIndicator = $('<div class="typing-indicator bot-message"><span></span><span></span><span></span></div>');
        $('.chat-messages').append(typingIndicator);
        $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
    }

    function removeTypingIndicator() {
        $('.typing-indicator').remove();
    }

    $('#chatbot-form-btn').click(function(e) {
        e.preventDefault();
        sendMessage();
    });

    $('#messageText').keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
            sendMessage();
        }
    });

    var isProcessing = false;

    function disableInput() {
        $('#messageText, #chatbot-form-btn, #chatbot-form-btn-voice, #chatbot-form-btn-pause, #toggle-upload-btn').prop('disabled', true);
    }

    function enableInput() {
        $('#messageText, #chatbot-form-btn, #chatbot-form-btn-voice, #chatbot-form-btn-pause, #toggle-upload-btn').prop('disabled', false);
    }

    function sendMessage() {
        var message = $('#messageText').val().trim();
        if (message && !isProcessing) {
            isProcessing = true;
            disableInput();

            appendMessage(message, true);
            $('#messageText').val('');
            showTypingIndicator();

            $.ajax({
                type: "POST",
                url: "/ask",
                data: { messageText: message },
                success: function(response) {
                    removeTypingIndicator();
                    if (response.error) {
                        appendMessage("Error: " + response.error, false);
                    } else {
                        var answer = response.answer;
                        appendMessage(answer, false);

                        if ($('#voiceReadingCheckbox').is(':checked')) {
                            msg.text = answer;
                            synth.speak(msg);
                        }
                    }
                    isProcessing = false;
                    enableInput();
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    removeTypingIndicator();
                    console.log(errorThrown);
                    appendMessage("Sorry, there was an error processing your request. Please try again later.", false);
                    isProcessing = false;
                    enableInput();
                }
            });
        }
    }

    // Image upload functionality
    $('#toggle-upload-btn').click(function() {
        $('#uploadForm').toggleClass('active');
    });

    $('#closeUpload').click(function() {
        $('#uploadForm').removeClass('active');
    });

    $('#selectImageBtn').click(function() {
        $('#imageFile').click();
    });

    $('#imageFile').change(function() {
        var file = this.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#imagePreview').attr('src', e.target.result).show();
                $('#uploadStatus').text(file.name);
                $('#submitImageBtn').prop('disabled', false);
            };
            reader.readAsDataURL(file);
        } else {
            $('#imagePreview').hide();
            $('#uploadStatus').text('No image selected');
            $('#submitImageBtn').prop('disabled', true);
        }
    });

    $('#imageUploadForm').submit(function(e) {
        e.preventDefault();
        if (!isProcessing) {
            var formData = new FormData();
            var fileInput = $('#imageFile')[0];
            
            if (fileInput.files.length > 0) {
                isProcessing = true;
                disableInput();
                $('#submitImageBtn').prop('disabled', true);
                
                formData.append('imageFile', fileInput.files[0]);
                
                // Display the image in the chat
                var imageUrl = URL.createObjectURL(fileInput.files[0]);
                appendMessage('', true, imageUrl);
                
                // Close the upload form
                $('#uploadForm').removeClass('active');
                showTypingIndicator();
                
                $.ajax({
                    type: "POST",
                    url: "/predict_disease",
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(response) {
                        removeTypingIndicator();
                        if (response.error) {
                            appendMessage("Error: " + response.error, false);
                        } else {
                            var answer = response.answer;
                            appendMessage(answer, false);

                            if ($('#voiceReadingCheckbox').is(':checked')) {
                                msg.text = answer;
                                synth.speak(msg);
                            }
                        }
                        
                        // Reset the form
                        $('#imageFile').val('');
                        $('#imagePreview').hide();
                        $('#uploadStatus').text('No image selected');
                        
                        isProcessing = false;
                        enableInput();
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        removeTypingIndicator();
                        console.log(errorThrown);
                        appendMessage("Sorry, there was an error processing your image. Please try again later.", false);
                        isProcessing = false;
                        enableInput();
                    }
                });
            }
        }
    });

    var welcomeMessage = "🌱🌾 Welcome to KrishiAI !! 🌾🌱 How can I assist you today? You can ask me agriculture questions or upload a plant leaf image for disease detection.";

    $('#chatbot-form-btn-clear').click(function(e) {
        e.preventDefault();
        $('.chat-messages').empty();
        appendMessage(welcomeMessage, false);
    });

    $('#chatbot-form-btn-voice').click(function(e) {
        e.preventDefault();

        if ('webkitSpeechRecognition' in window && !isProcessing) {
            var recognition = new webkitSpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.start();

            recognition.onresult = function(event) {
                var speechResult = event.results[0][0].transcript;
                $('#messageText').val(speechResult);
                sendMessage();
            };

            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
            };
        } else {
            console.log('Web Speech API is not supported in this browser or processing is in progress');
        }
    });

    $('#voiceReadingCheckbox').change(function() {
        if (!$(this).is(':checked')) {
            synth.cancel();
        }
    });

    // PAUSE BUTTON FUNCTIONALITY
    $('#chatbot-form-btn-pause').click(function() {
        stopTyping(); // Stops text from typing
        synth.cancel(); // Stops voice reading
    });

    // Initialize voice
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = setVoice;
    }
    setVoice();

    setTimeout(function() {
        appendMessage(welcomeMessage, false);
    }, 500);
});


