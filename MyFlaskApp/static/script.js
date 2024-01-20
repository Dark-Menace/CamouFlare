angular.module('steganographyApp', [])
        .controller('SteganographyController', ['$scope','$http', function($scope,$http) {
            $scope.selectedImage = null;
            $scope.message = '';
            $scope.decodedMessage = '';
            $scope.errorMessage='';
            $scope.showAlert = false;
            $scope.textAreaDisabled=true;
            $scope.buttonDisabled=true;

            $scope.closeAlert=function(){
                $scope.showAlert=false;
                $scope.errorMessage="";
                $scope.textAreaDisabled=false;
                $scope.buttonDisabled=false;
            };

            $scope.handleImageSelect = function() {                
                $scope.selectedImage = document.getElementById('imageInput').files[0];// Handle image selection if needed
                $scope.textAreaDisabled=false;
                $scope.buttonDisabled=false;
            };

            $scope.resetPage = function () {
            window.location.reload();
            };

            $scope.encodeMessage = function() {
                var formData = new FormData();
                formData.append('file', $scope.selectedImage);
                formData.append('textData', $scope.message);
    // Make an HTTP POST request to Flask
                $http.post('http://127.0.0.1:5000/encode', formData, {
                responseType: 'arraybuffer',
                transformRequest: angular.identity,
                headers: { 'Content-Type': undefined }  // Use undefined instead of formData
                })
                .then(function(response) {
        // Handle success
                console.log(response.data);

        // Check if the response contains an image 
                if (response.data) {
                downloadImage(response.data, 'processed_image.png');
                console.log(response.data.result);
                }
            })
                .catch(function(error) {
        // Handle error
                // Convert the buffer stream to a string
                var jsonString = String.fromCharCode.apply(null, new Uint8Array(error.data));

                // Parse the JSON string to a JavaScript object
                var jsonData = JSON.parse(jsonString);

                    
                console.error('Error:', jsonData.result);
                //console.error(error.data.result);
                $scope.errorMessage= jsonData.result;
                $scope.showAlert = true;
                $scope.textAreaDisabled=true;
                $scope.buttonDisabled=true;
            });
            };
        function downloadImage(imageData, filename) {
    // Convert the base64 image data to a Blob
            var blob = new Blob([imageData], { type: 'image/png' });

    // Create a downloadable link
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = filename;
            document.body.appendChild(link);

    // Trigger the download
            link.click();

    // Remove the link from the DOM
            document.body.removeChild(link);
        }

            $scope.decodeMessage = function(event) {
                event.preventDefault();
                var formData = new FormData();
                formData.append('file', $scope.selectedImage);
                $http.post('http://127.0.0.1:5000/decode', formData, {
                Accept: 'application/json',
                transformRequest: angular.identity,
                headers: { 'Content-Type': undefined }  // Use undefined instead of formData
                })
                .then(function(response) {
        // Handle success
                console.log(response.data);

                if (response.data) {
                    console.log(response.data.dataFound);
                    $scope.decodedMessage = response.data.dataFound
                    
                }

            })
                .catch(function(error) {
        // Handle error
                console.error('Error:', error);
                $scope.errorMessage = error.data.result;
                $scope.showAlert = true;
                console.error(error.data.result);
                $scope.textAreaDisabled=true;
                $scope.buttonDisabled=true;
                
                
            });
            
            };


        }]);
