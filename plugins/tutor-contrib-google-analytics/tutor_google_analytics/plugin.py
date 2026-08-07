from tutor import hooks
from tutormfe.hooks import EXTERNAL_SCRIPTS


# This snippet is inlined verbatim into both a .jsx and a .tsx file, so it has
# to be plain JavaScript that also survives the frontend-base type checker:
# no implicit `this` properties, no undeclared globals, no possibly-null DOM
# nodes.
GOOGLE_ANALYTICS_LOADER = """
class GoogleAnalyticsLoader {
  analyticsId = '';

  constructor({ config }) {
    this.analyticsId = config.GOOGLE_ANALYTICS_4_ID;
  }

  loadScript() {
    if (!this.analyticsId) {
      return;
    }

    // Never inject the snippet twice, in case more than one app registers
    // the loader on the same page.
    if (document.querySelector('script[data-google-analytics-4]')) {
      return;
    }

    const scriptSrc = document.createElement('script');
    scriptSrc.async = true;
    scriptSrc.src = `https://www.googletagmanager.com/gtag/js?id=${this.analyticsId}`;
    scriptSrc.setAttribute('data-google-analytics-4', '');

    const scriptGtag = document.createElement('script');
    scriptGtag.innerHTML = `
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '${this.analyticsId}');
    `;

    document.head.appendChild(scriptSrc);
    document.head.appendChild(scriptGtag);
  }
}
"""


# Inline the loader into both build pipelines: env.config.jsx for legacy MFEs,
# customApp.tsx for the frontend-base site.
hooks.Filters.ENV_PATCHES.add_item(
    ("mfe-env-config-buildtime-definitions", GOOGLE_ANALYTICS_LOADER)
)
hooks.Filters.ENV_PATCHES.add_item(
    ("mfe-site-custom-app-definitions", GOOGLE_ANALYTICS_LOADER)
)

# Register the loader for both targets ("all" covers legacy MFEs and the site).
EXTERNAL_SCRIPTS.add_item(("all", "GoogleAnalyticsLoader"))
