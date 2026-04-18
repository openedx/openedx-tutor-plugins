from tutor import hooks
from tutormfe.hooks import EXTERNAL_SCRIPTS


GOOGLE_ANALYTICS_LOADER = """
class GoogleAnalyticsLoader {
  constructor({ config }) {
    this.analyticsId = config.GOOGLE_ANALYTICS_4_ID;
  }

  loadScript() {
    if (!this.analyticsId) {
      return;
    }

    global.googleAnalytics = global.googleAnalytics || [];
    const { googleAnalytics } = global;

    // If the snippet was invoked do nothing.
    if (googleAnalytics.invoked) {
      return;
    }

    // Invoked flag, to make sure the snippet
    // is never invoked twice.
    googleAnalytics.invoked = true;

    googleAnalytics.load = (key, options) => {
      const scriptSrc = document.createElement('script');
      scriptSrc.type = 'text/javascript';
      scriptSrc.async = true;
      scriptSrc.src = `https://www.googletagmanager.com/gtag/js?id=${key}`;

      const scriptGtag = document.createElement('script');
      scriptGtag.innerHTML = `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '${key}');
      `;

      // Insert our scripts next to the first script element.
      const first = document.getElementsByTagName('script')[0];
      first.parentNode.insertBefore(scriptSrc, first);
      first.parentNode.insertBefore(scriptGtag, first);
      googleAnalytics._loadOptions = options; // eslint-disable-line no-underscore-dangle
    };

    // Load GoogleAnalytics with your key.
    googleAnalytics.load(this.analyticsId);
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
