var app = angular.module('scriptweb', []);


app.controller('scriptwebController', function($scope, $window, $http, $timeout) {


    $scope.contact_form = function() {
        if ($scope.name == undefined || $scope.email == undefined || $scope.msg == undefined) {
            alert('Please Fill The Details');
            return;
        }
        $http({
            method: "POST",
            url: "/contact/contactus/",
            data: { 'name': $scope.name, 'email': $scope.email, 'msg': $scope.msg }
        }).then(
            function(success) {
                console.log(success.data);
                $scope.success = success.data.message;
                toast();
                $scope.succ = true;
                $timeout(function() {
                    $scope.succ = false;
                }, 10000);
                // $scope.correct()
                alert('Email Sent');
            },
            function(error) {
                $scope.error = error.data["message"];
                alert(error.data['message']);
            });
    };

});