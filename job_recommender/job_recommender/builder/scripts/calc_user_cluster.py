import os
from itertools import groupby
from tqdm import tqdm

import django
from django.db.models import Count

from scipy.sparse import dok_matrix
from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA
# import matplotlib as mlt
# import matplotlib.pyplot as plt

import numpy as np


from ...analytics.models import Rating, Cluster


BATCH_SIZE = 4000

# def plot(user_ratings, kmeans, k):
#         print("reduce dimensionality of data")
#         h = 0.2
#         reduced_data = PCA(n_components=2).fit_transform(user_ratings)
#         print("cluster reduced data")

#         if not kmeans:
#             kmeans = KMeans(init='k-means++', n_clusters=k, n_init=10)
#             kmeans.fit(reduced_data)

#         print("plot clustered reduced data")
#         x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
#         y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
#         xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

#         Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

#         # Put the result into a color plot
#         Z = Z.reshape(xx.shape)

#         plt.figure(1)
#         plt.clf()
#         plt.imshow(Z, interpolation='nearest',
#                    extent=(xx.min(), xx.max(), yy.min(), yy.max()),
#                    cmap=plt.cm.Paired,
#                    aspect='auto', origin='lower')

#         centroids = kmeans.cluster_centers_
#         plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
#         plt.scatter(centroids[:, 0], centroids[:, 1],
#                     marker='x', s=169, linewidths=3,
#                     color='w', zorder=10)
#         plt.title('K-means clustering of the user')
#         plt.xlim(x_min, x_max)
#         plt.ylim(y_min, y_max)
#         plt.xticks(())
#         plt.yticks(())

#         plt.savefig('cluster.png')


class UserClusterCalculator(object):


    def calculate(self, k = 23):
        print("training k-means clustering")

        user_ids, user_ratings = self.load_data()

        kmeans = KMeans(n_clusters=k)

        clusters = kmeans.fit(user_ratings.tocsr())

        # plot(user_ratings.todense(), kmeans, k)

        self.save_clusters(clusters, user_ids)

        return clusters


    @staticmethod
    def save_clusters(clusters, user_ids):
        print("saving clusters")

        bulk_list = []
        Cluster.objects.all().delete()
        for i, cluster_label in tqdm(enumerate(clusters.labels_)):
            cluster = Cluster(
                        type='customer',
                        cluster_id=cluster_label,
                        source_id=user_ids[i]['customer_id'])
            bulk_list.append(cluster)

            if i % BATCH_SIZE == 0:
                Cluster.objects.bulk_create(bulk_list)
                bulk_list = []


    @staticmethod
    def load_data():
        print('loading data')
        user_ids = list(
            Rating.objects.values('customer_id')
                .annotate(company_count=Count('company_id'))
                .order_by('-company_count'))
        # user_ids:
        # [{'customer_id': 189948, 'company_count': 8},
        #  {'customer_id': 1101440, 'company_count': 8}]

        content_ids = list(Rating.objects.values('company_id').distinct())
        # content_ids:
        # [{'company_id': 48892},
        #  {'company_id': 46875}]

        num_users = len(user_ids)
        num_contents = len(content_ids)
        print('num_users:', num_users)
        print('num_contents:', num_contents)

        content_map = {content_ids[i]['company_id']: i
                       for i in range(num_contents)}
        # content_map:               
        # {48892: 0, 305940: 1, 149418: 2, 156456: 3, 46875: 4}
        user_ratings = dok_matrix((num_users, num_contents), dtype=np.float32)

        customer_map = {}
        all_ratings = list(Rating.objects.values('customer_id','company_id','rating'))
        all_ratings.sort(key=lambda x: x['customer_id'])

        for k,v in groupby(all_ratings,key=lambda x: x['customer_id']):
            customer_map[k] = list(v)

        # customer_map:  
        # {
        # 1193206: [{'customer_id': 1193206, 'company_id': 230909, 'rating': Decimal('5.86')}]
        # 1193218: [{'customer_id': 1193218, 'company_id': 138604, 'rating': Decimal('3.98')}, {'customer_id': 1193218, 'company_id': 180092, 'rating': Decimal('6.37')}]
        # }

        for i in tqdm(range(num_users)):
            customer_id=user_ids[i]['customer_id']
            ratings = customer_map[customer_id]
            
            for user_rating in ratings:
                j = content_map[user_rating['company_id']]
                user_ratings[i, j] = user_rating['rating']

        print('data loaded')

        return user_ids, user_ratings


def run():
    print("Calculating clusters...")

    cluster = UserClusterCalculator()
    cluster.calculate(23)
