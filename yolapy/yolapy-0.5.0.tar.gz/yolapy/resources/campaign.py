class CampaignResourceMixin(object):
    """Methods for managing Campaign resources."""

    def list_campaigns(self, site_id, **options):
        """Return list of campaigns for a site."""
        return self.get(self._campaign_path(site_id), params=options).json()

    def get_campaign(self, site_id, campaign_id):
        """Return details for a particular campaign.

        >>> campaign = yola.get_campaign('site_id', 'campaign_id')
        >>> campaign['name']
        'My Campaign'
        """
        return self.get(self._campaign_path(site_id, campaign_id)).json()

    def delete_campaign(self, site_id, campaign_id):
        """Delete a campaign."""
        self.delete(self._campaign_path(site_id, campaign_id))

    def _campaign_path(self, site_id, *parts):
        path = '/'.join(['sites', site_id, 'campaigns'] + list(parts))
        return '/%s/' % path
