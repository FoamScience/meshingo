import { defineConfig } from 'unocss'

export default defineConfig({
  preflights: [
    {
      layer: 'base', // This applies your variables globally in the base layer
      getCSS: () => `
        :root {
          --slidev-theme-primary: #2f5061;
          --slidev-theme-secondary: #4297a0;
          --slidev-theme-warn: #18a558;
          --slidev-theme-error: #df362d;
          --slidev-theme-mermaid-text-color: #ffffff;
          --slidev-theme-mermaid-axis-font-size: 20;
          --slidev-theme-mermaid-axis-scale-factor: 0.5;
          --slidev-theme-mermaid-curve-tension: 0.1;
          --slidev-theme-mermaid-radar-width: 800;
          --slidev-theme-mermaid-radar-height: 600;
        }
      `,
    },
  ],
})
