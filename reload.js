module.exports = async function(context, commands) {
  let url = context.options.browsertime.url;
  await commands.navigate('https://en.wikipedia.org/wiki/Barack_Obama');
  await commands.wait.byTime(3000);
  await commands.navigate(url);
  await commands.wait.byTime(5000);
  await commands.navigate('about:blank');
  await commands.wait.byTime(2000);
  return commands.measure.start(url);
};
