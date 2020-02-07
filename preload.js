module.exports = async function(context, commands) {
  let url = context.options.browsertime.url;
  // Conditioning disabled until we can prove that it reduces noise
  // await commands.navigate('https://www.example.com');
  // await commands.wait.byTime(30000);
  // await commands.navigate('about:blank');
  // await commands.wait.byTime(5000);
  return commands.measure.start(url);
};
