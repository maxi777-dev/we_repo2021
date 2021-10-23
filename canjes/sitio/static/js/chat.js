function refresh_chat(id, user){
    fetch("/chat/"+id)
        .then(response => response.json())
        .then(data => add_messages(data, user));
    $('#form_add_message').attr('action', '/chat/' + id);
}

function add_messages(data, user) {
    var messages = '';
    $.each(data, function(val, text) {
        if (user == text.sender){
            messages +=
                `<div class="media w-50 mb-3"><img src="https://bootstrapious.com/i/snippets/sn-chat/avatar.svg" alt="user" width="50" class="rounded-circle">
                <div class="media-body ml-3">
                  <div class="bg-light rounded py-2 px-3 mb-2">
                    <p class="text-small mb-0 text-muted">` + text.content + `</p>
                  </div>
                  <p class="small text-muted">` + text.timestamp + `</p>
                </div>
              </div>`;
        }else{
            messages +=
                `<div class="media w-50 ml-auto mb-3">
                    <div class="media-body">
                    <div class="bg-primary rounded py-2 px-3 mb-2">
                        <p class="text-small mb-0 text-white">` + text.content + `</p>
                    </div>
                    <p class="small text-muted">` + text.timestamp + `</p>
                    </div>
                </div>`;
        }
    });
    $("#conteiner_chat_messages").html(messages);
  }