(function () {
  console.log("loading Neuria toobar.");

  const config = {};

  function retriveConfig() {
    console.log("Loading Neuria config to toobar.");

    function onError(error) {
      console.log(`Error: ${error}`);
    }
    function onGot(result) {
      if (result && result.config) {
        for (let key of Object.keys(result.config)) {
          config[key] = result.config[key];
        }
        console.log("Loaded Neuria config to toobar.");
        console.log(config);

        try {
          displayConfig();
        } catch (e) {
          console.log(e);
        }
      } else {
        console.log("Config stored is missing or borken, this is unexpected.");

        return;
      }
    }

    let getting = browser.storage.sync.get("config");
    getting.then(onGot, onError);
  }

  browser.storage.onChanged.addListener((change, areaName) => {
    console.log("Received config change event.");
    retriveConfig();
  });
  retriveConfig();

  function displayConfig() {
    let selectStatus = document.getElementById("__Neuria_select_status__");
    if (!selectStatus) {
      console.log("no selectStatus");
      return;
    }
    selectStatus.value = config.status;

    let inputNodes = document.getElementsByTagName("input");

    for (let inputNode of inputNodes) {
      inputNode.value = config[inputNode.name];
    }
  }

  window.addEventListener("load", (event) => {
    let selectStatus = document.getElementById("__Neuria_select_status__");
    if (!selectStatus) {
      console.log("no selectStatus");
      return;
    }
    selectStatus.onchange = function (e) {
      let index = e.target.selectedIndex;
      let value = e.target.options[index].value;

      config.status = value;

      browser.storage.sync.set({ config: config });
    };

    let inputNodes = document.getElementsByTagName("input");

    for (let inputNode of inputNodes) {
      inputNode.addEventListener("input", updateValue);

      function updateValue(e) {
        console.log("Received input change event.");
        config[inputNode.name] = e.target.value;

        browser.storage.sync.set({ config: config });
      }
    }

    console.log("Neuria toobar is fully loaded");
  });
})();
