var app = angular.module('scriptmodule', []);


app.controller('scriptcontroller', function($scope, $window, $http, $timeout) {

    $scope.creating_user = function(x = true) {
        // $scope.signup_firstname = 'test'
        // $scope.signup_lastname = 'test'
        // $scope.signup_email = 'arpitsodhi@hotmail.co.uk'
        // $scope.signup_password = '123456'

        if ($scope.signup_firstname == undefined || $scope.signup_lastname == undefined || $scope.signup_email == undefined || $scope.signup_password == undefined || $scope.signup_cfpassword == undefined) {
            alert('Please Fill The Details Properly');
            return;
        }
        // var str = $scope.signup_password;
        // if (str.match(/[a-z]/g) && str.match( 
        //     /[A-Z]/g) && str.match( 
        //     /[0-9]/g) && str.match( 
        //     /[^a-zA-Z\d]/g) && str.length >= 8){
        //     }
        // else{
        //     alert('Weak password \n \n Please use: \n 1.) At least 1 uppercase character. \n 2.) At least 1 lowercase character. \n 3.) At least 1 digit. \n 4.) At least 1 special character. \n 5.) Minimum 8 characters.');
        //     return
        // }
        if (!x) {
            return;
        }
        $http({
            method: "POST",
            url: "/invited_user/",
            data: { 'firstname': $scope.signup_firstname, 'lastname': $scope.signup_lastname, 'password': $scope.signup_password, 'email': $scope.signup_email }
        }).then(
            function(success) {
                $scope.success = success.data.message;
                $scope.succ = true;
                $scope.success = "Saved";
                $scope.signup_firstname = '';
                $scope.signup_lastname = '';
                $scope.signup_email = '';
                $scope.signup_password = '';
                $timeout(function() {
                    $scope.succ = false;
                }, 10000);
                // $scope.correct()
                // window.location='/marketplace/';
                alert('Check your mail to activate !!');
            },
            function(error) {
                $scope.showerror = true;
                $scope.err = true;
                $timeout(function() {
                    $scope.showerror = false;
                }, 10000);
                $scope.error = error.data["message"];
                alert(error.data['message']);
            });
    };
    $scope.login_function = function() {
        // $scope.username = 'arpitsodhi@hotmail.co.uk'
        // $scope.password = '12345678'
        if ($scope.username == undefined || $scope.password == undefined) {
            alert('Please Fill The Details');
            return;
        }
        $http({
            method: "POST",
            url: "/login/",
            data: { 'username': $scope.username, 'password': $scope.password }
        }).then(
            function(success) {
                console.log(success.data);
                $scope.success = success.data.message;
                $scope.succ = true;
                $scope.username = '';
                $scope.password = '';
                $timeout(function() {
                    $scope.succ = false;
                }, 10000);
                window.location = '/home/';
            },
            function(error) {
                $scope.showerror = true;
                console.log(error.data);
                $scope.err = true;
                $timeout(function() {
                    $scope.showerror = false;
                }, 10000);
                $scope.error = error.data["message"];
                alert(error.data['message']);
            });
    };
});