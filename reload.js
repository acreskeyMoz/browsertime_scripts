module.exports = async function(context, commands) {
  let url = context.options.browsertime.url;
  await commands.navigate('https://www.mozilla.org/en-US/');
  await commands.wait.byTime(3000);
  await commands.navigate(url);
  await commands.wait.byTime(8000);
  return commands.measure.start(url);
};
