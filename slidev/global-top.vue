<!-- global-top.vue -->
<template>
    <div class="absolute top-6 right-6">
    <LightOrDark>
      <template #dark>
      <img 
        :src="$slidev.themeConfigs.darkLogo" 
        class="slidev-image" 
        :width="$slidev.themeConfigs.logoWidth" 
        alt="Dark-Logo"
      />
      </template>
      <template #light>
      <img 
        :src="$slidev.themeConfigs.logo" 
        class="slidev-image" 
        :width="$slidev.themeConfigs.logoWidth" 
        alt="Logo"
      />
      </template>
    </LightOrDark>
    </div>
</template>
