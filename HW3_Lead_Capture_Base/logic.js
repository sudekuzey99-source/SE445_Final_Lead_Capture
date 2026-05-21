// Process incoming HTTP POST data and extract name, email, and message
let results = [];

for (const item of $input.all()) {
  let name = item.json.body?.name || "No name provided";
  let email = item.json.body?.email || "No email provided";
  let message = item.json.body?.message || "No message provided";
  
  results.push({
    json: {
      name: name,
      email: email,
      message: message,
      processedAt: new Date().toISOString()
    }
  });
}

return results;