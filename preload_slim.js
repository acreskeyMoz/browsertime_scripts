module.exports = async function(context, commands) {
  let url = context.options.browsertime.url;
  return commands.measure.start(url);
};
