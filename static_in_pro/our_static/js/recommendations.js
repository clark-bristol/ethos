// var jsonStr=document.getElementById('test_json').innerHTML;
// var json=JSON.stringify(jsonStr);
// var test_json=JSON.parse(json);
// console.log(test_json);


Vue.component('claim-box', {
  template: '#claim-box-template',
  props: ['claim','user'],
  methods: {
    toggleEditing: function () {
      if (this.claim.editing === false) {
        this.claim.editing = true;
      }
      else {
        this.claim.editing = false;
      }
    },
    cancelEditing: function () {
      // this.message = this.message.split('').reverse().join('');
      this.claim.editing = false;
    },
    toggleAffirmation: function() {
      if (!this.claim.affirmation_id) {
        console.log('blank');
        var data = JSON.stringify({ "claim" : this.claim.id, "user" : this.user.id, "csrf_token" : csrftoken });
        // console.log(data);
        element = this;
        $.ajax({
          "type": "POST",
          "dataType": "json",
          "url": "http://localhost:8000/api/affirmations/",
          "data": data,
          "contentType": "application/json",
          "success": function(result) {
            element.claim.affirmation_id = result.id;
            console.log("Affirmed!");
          },
        });
      }
      else {
        console.log('not blank');
        var url = "http://localhost:8000/api/affirmations/".concat(this.claim.affirmation_id.toString()).concat("/");
        element = this;
        $.ajax( {
            "type": "DELETE",
            "url": url,
            "success": function(result) {
              element.claim.affirmation_id = '';
              console.log("Un-Affirmed!");
            },
        });
      }
    },
    saveClaim: function() {
      var data = JSON.stringify({ "id" : this.claim.id,
                                  "name" : this.claim.name,
                                  "content" : this.claim.content,
                                  // "csrf_token" : csrftoken
                                });
      console.log(data);
      // console.log(data);
      element = this;
      $.ajax({
        "type": "PUT",
        "dataType": "json",
        "url": "http://localhost:8000/api/claims/".concat(this.claim.id).concat("/"),
        "data": data,
        "contentType": "application/json",
        "success": function(result) {
          element.claim.id = result.id;
          console.log("Claim Updated!");
        },
      });
      this.toggleEditing();
    }
  }
});

var vm = new Vue(test_json);
