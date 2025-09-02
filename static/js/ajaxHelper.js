class AjaxHelper {
  static get(url, onSuccess, onError) {
    fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => onSuccess(data))
      .catch((error) => {
        console.error("AjaxHelper GET error:", error);
        if (onError) onError(error);
      });
  }

  static post(url, data, onSuccess, onError) {
    fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => onSuccess(data))
      .catch((error) => {
        console.error("AjaxHelper POST error:", error);
        if (onError) onError(error);
      });
  }

  static put(url, data, onSuccess, onError) {
    fetch(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => onSuccess(data))
      .catch((error) => {
        if (onError) onError(error);
      });
  }

  static delete(url, onSuccess, onError) {
    fetch(url, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => response.json())
      .then((data) => onSuccess(data))
      .catch((error) => {
        if (onError) onError(error);
      });
  }
}
