import { defineMermaidSetup } from '@slidev/types'

const getSlidevCssVariables = () => {
  const rootStyles = getComputedStyle(document.documentElement);
  const slidevVariables = {};
  for (let i = 0; i < rootStyles.length; i++) {
    const property = rootStyles[i];
    slidevVariables[property] = rootStyles.getPropertyValue(property);
  }
  return slidevVariables;
}

export default defineMermaidSetup(async () => {
  const isDark = document.documentElement.classList.contains('dark');
  const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--slidev-theme-primary').trim()
  const secondaryColor = getComputedStyle(document.documentElement).getPropertyValue('--slidev-theme-secondary').trim()
  const tertiaryColor = getComputedStyle(document.documentElement).getPropertyValue('--slidev-theme-warn').trim()
  //console.log(getSlidevCssVariables())
  const font = getComputedStyle(document.documentElement).getPropertyValue('font-family').trim()
  const fontSize = getComputedStyle(document.documentElement).getPropertyValue('font-size').trim()
  const textColor = getComputedStyle(document.documentElement).getPropertyValue('--slidev-theme-mermaid-text-color').trim()
  const axisFontSize = getComputedStyle(document.documentElement).getPropertyValue('--slidev-theme-mermaid-axis-font-size').trim()
  const radarWidth = getComputedStyle(document.documentElement).getPropertyValue('--slidev-theme-mermaid-radar-width').trim()
  const radarHeight = getComputedStyle(document.documentElement).getPropertyValue('--slidev-theme-mermaid-radar-height').trim()
  const theme = {
    theme: 'base',
    radar: {
      axisScaleFactor: getComputedStyle(document.documentElement).getPropertyValue('--slidev-theme-mermaid-axis-scale-factor').trim(),
      curveTension: getComputedStyle(document.documentElement).getPropertyValue('--slidev-theme-mermaid-curve-tension').trim(),
      width: radarWidth,
      height: radarHeight,
    },
    themeVariables: {
      darkMode: isDark,
      primaryColor: primaryColor,
      secondaryColor: secondaryColor,
      tertiaryColor: tertiaryColor,
      fontFamily: font,
      fontSize: fontSize,
      axisLabelFontSize: axisFontSize,
      cScale0: primaryColor,
      cScale1: secondaryColor,
      cScale2: tertiaryColor,
      cScale3: primaryColor,
      cScale4: secondaryColor,
      cScale5: tertiaryColor,
      xyChart: {
        plotColorPalette: [primaryColor, secondaryColor, tertiaryColor].join(',')
      },
      radar: {
        legendFontSize: axisFontSize,
        legendBoxSize: 30,
        axisLabelFontSize: axisFontSize,
      },
    }
  }
  if (textColor) {
    theme.themeVariables.nodeTextColor = textColor;
    theme.themeVariables.labelTextColor = textColor;
    theme.themeVariables.labelColor = textColor;
    theme.themeVariables.classText = textColor;
  }
  return theme
})
