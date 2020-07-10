module.exports = async function(context, commands) {
  let url = context.options.browsertime.url;
  
  await commands.navigate('https://www.mozilla.org/en-US/');
  await commands.wait.byTime(10000);
  await commands.navigate('about:blank');
  await commands.wait.byTime(5000);
  return commands.measure.start(url);
};
