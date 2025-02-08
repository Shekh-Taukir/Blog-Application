document.getElementById("blogs_title").focus();

async function of_load_blog_data() {
    const blog_tran_id = sessionStorage.getItem("blog_edit_tran_id");

    try {
        const response = await fetch(main_api + blogs_api_point + `Get Blog?blog_id=${blog_tran_id}`);

        if (response.ok) {
            const data = await response.json();

            document.getElementById("blogs_title").value = data.result.blog_title;
            document.getElementById("blogs_description").value = data.result.blog_description;
        }
        else {
            alert("An error occured while fetching blog data!!");
            of_return_to_index();
        }
    }
    catch (error) {
        alert("Error occured while fetching blog data");
        of_return_to_index();
    }
}

function of_update_data() {
    document.getElementById("edit_blog_form").addEventListener("submit", async function (event) {
        event.preventDefault();

        const blog_tran_id = sessionStorage.getItem("blog_edit_tran_id");

        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch(main_api + blogs_api_point + `Update Blog?blog_id=${blog_tran_id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });
            if (!(response.ok)) {
                alert("Failed to update data!!!");
            }
            else {
                alert("Data updated with success!!!");
            }
        } catch (error) {
            console.error("Errr:" + error);
            alert("Failed to update data!!!");
        }
        of_return_to_index();
    });
}

of_load_blog_data();
of_update_data();