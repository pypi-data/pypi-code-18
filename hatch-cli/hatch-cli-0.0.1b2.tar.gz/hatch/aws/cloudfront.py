

# TODO: Create certificate. ACM is the name of the service.
client.create_distribution(
    DistributionConfig={
        'Origins': {
            'DefaultRootObject': 'index.html'
            'Items': [
                'DomainName': 'hatch.sh.s3.amazonaws.com'
            ]
        },
        'Aliases'={
            'Quantity': 2,
            'Items': [
                'www.hatch.com',
                'hatch.com'
            ]
        }
    },

)
