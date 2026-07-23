// Netlify Function — Stripe Checkout Session
// Deploy this with Netlify. Set env var STRIPE_SECRET_KEY in Netlify dashboard.
// Stripe SDK is auto-installed by Netlify when it sees 'require("stripe")'

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event) => {
  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { price, name, tier, months, discountPct } = JSON.parse(event.body);

    if (!price || !name) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Missing price or name' }) };
    }

    const amount = Math.round(parseFloat(price) * 100); // Stripe uses cents
    if (amount <= 0) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Invalid price' }) };
    }

    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      success_url: `${process.env.URL || 'https://capo-horn-lab.github.io/capohornlab-website'}/dashboard.html?paid=1`,
      cancel_url: `${process.env.URL || 'https://capo-horn-lab.github.io/capohornlab-website'}/checkout.html?canceled=1`,
      line_items: [
        {
          price_data: {
            currency: 'eur',
            product_data: {
              name: name || 'Strategy Backtest',
              description: `Tier: ${tier || 'L2'} · ${months || 12} months${discountPct ? ' · ' + discountPct + '% off' : ''}`,
            },
            unit_amount: amount,
          },
          quantity: 1,
        },
      ],
      metadata: {
        tier: tier || 'l2',
        months: String(months || 12),
        strategy: name || '',
        discount: discountPct ? String(discountPct) : '',
      },
    });

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sessionId: session.id }),
    };
  } catch (err) {
    console.error('Stripe Checkout error:', err);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message }),
    };
  }
};
